from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from backend.data.generator import main as generator_main, stop_generator
from backend.db.db_manager import get_all_data, get_data_from_table, get_latest_data, get_table_names, get_column_names
from backend.api.plot_utils import plot_linear, plot_moving_average, plot_trend_line, plot_derivative, plot_spectrum, plot_histogram, plot_heatmap, plot_scatter
from typing import Dict, List
from pathlib import Path
import threading, asyncio, logging


logger = logging.getLogger("routes")
router = APIRouter()
active_connections: Dict[str, List[WebSocket]] = {}

generator_thread = None
generator_running = False


 # – Генератор –
def generator_wrapper():
    global generator_running
    generator_running = True
    try:
        generator_main()
    finally:
        generator_running = False


@router.post("/generator/start")
async def start_generator():
    global generator_thread, generator_running
    if generator_thread is None or not generator_thread.is_alive():
        generator_thread = threading.Thread(target=generator_wrapper)
        generator_thread.start()
        return {"status": "Generator started"}
    else:
        return {"status": "Generator is already running"}


@router.post("/generator/stop")
async def stop_generator_route():
    global generator_running
    if generator_running:
        stop_generator()
        generator_thread.join()
        generator_running = False
        return {"status": "Generator stopped"}
    else:
        return {"status": "Generator is not running"}


 # – Пути к страничкам –
@router.get("/", response_class=HTMLResponse)
async def home_page():
    home_path = Path(__file__).parent.parent.parent / "web/templates/home.html"
    home_content = home_path.read_text(encoding="utf-8")
    return HTMLResponse(content=home_content, status_code=200)


@router.get("/SfPTPfS", response_class=HTMLResponse)
async def SfPTPfS_page():
    SfPTPfS_path = Path(__file__).parent.parent.parent / "web/templates/SfPTPfS.html"
    SfPTPfS_content = SfPTPfS_path.read_text(encoding="utf-8")
    return HTMLResponse(content=SfPTPfS_content, status_code=200)


@router.get("/monitoring", response_class=HTMLResponse)
async def monitoring_page():
    monitoring_path = Path(__file__).parent.parent.parent / "web/templates/monitoring.html"
    monitoring_content = monitoring_path.read_text(encoding="utf-8")
    return HTMLResponse(content=monitoring_content, status_code=200)


 # – Данные с датчиков –
@router.get("/units")
async def get_units():
    try:
        units = get_table_names()
        return {"units": units}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving units.")


@router.get("/parameters/{unit}")
async def get_parameters(unit: str):
    try:
        parameters = get_column_names(unit)
        return {"parameters": parameters}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving parameters for the selected unit.")


 # – Графики –
@router.get("/plot/{unit}/{parameter}/{graph_type}")
async def get_plot(unit: str, parameter: str, graph_type: str, start_time: str, end_time: str):
    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Дата начала не может быть позднее даты конца или наоборот.")

    data = get_data_from_table(unit, parameter, start_time, end_time)

    if not data:
        raise HTTPException(status_code=404, detail="Данные за указанный период отсутствуют.")

    plot_function = {
        "linear": plot_linear,
        "moving_avg": plot_moving_average,
        "trend_line": plot_trend_line,
        "derivative": plot_derivative,
        "fft": plot_spectrum,
        "histogram": plot_histogram,
        "heatmap": plot_heatmap,
        "scatter": plot_scatter
    }.get(graph_type)

    if not plot_function:
        raise HTTPException(status_code=400, detail="Недопустимый тип графика.")

    plot_path = plot_function(data, [parameter], unit=unit, parameter=parameter, format="svg")

    return FileResponse(plot_path, media_type="image/svg+xml")


 # – Web –
async def send_all_data(websocket: WebSocket, unit: str, parameter: str):
    try:
        data = get_all_data(unit, parameter)
        for entry in data:
            await websocket.send_json({
                "time": entry["registered_value"].strftime('%Y-%m-%d %H:%M:%S'),
                "value": entry[parameter]
            })
    except Exception as e:
        print(f"Error sending initial data: {e}")


async def send_data(websocket: WebSocket, unit: str, parameter: str):
    while True:
        try:
            data = get_latest_data(unit, parameter)
            if data:
                await websocket.send_json({
                    "time": data["registered_value"].strftime('%Y-%m-%d %H:%M:%S'),
                    "value": data[parameter]
                })
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error sending data: {e}")
            break


@router.websocket("/ws/{unit}/{parameter}")
async def websocket_endpoint(websocket: WebSocket, unit: str, parameter: str):
    await websocket.accept()

    try:
        await send_all_data(websocket, unit, parameter)

        await send_data(websocket, unit, parameter)
    except WebSocketDisconnect:
        print("Client disconnected")


 # – Корневой маршрут –
@router.get("/")
async def root():
    return {"message": "Service is running!"}