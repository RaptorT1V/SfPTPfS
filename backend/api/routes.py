from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

from backend.data.generator import main as generator_main, stop_generator
from backend.db.db_manager import get_data_from_table
from backend.api.plot_utils import plot_linear, plot_moving_average, plot_trend_line, plot_derivative, plot_spectrum, plot_histogram, plot_heatmap, plot_scatter

from pathlib import Path
import threading, asyncio, logging


logger = logging.getLogger("routes")
router = APIRouter()

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

    # Вызов соответствующей функции построения графика
    plot_path = plot_function(data, [parameter], unit=unit, parameter=parameter, format="svg")

    return FileResponse(plot_path, media_type="image/svg+xml")


 # – Web –
@router.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = Path(__file__).parent.parent.parent / "web/templates/index.html"
    index_content = index_path.read_text(encoding="utf-8")
    return HTMLResponse(content=index_content, status_code=200)

'''
@router.websocket("/ws/plot/{unit}/{parameter}")
async def websocket_plot(websocket: WebSocket, unit: str, parameter: str):
    await websocket.accept()
    while True:
        data = get_data_from_table(unit, parameter, start_time=get_newest_timestamp(unit))
        await websocket.send_json(data)
        await asyncio.sleep(2)
'''

 # – Данные датчиков –
@router.get("/data/{table_name}")
async def get_sensor_data(table_name: str):
    try:
        data = get_data_from_table(table_name)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/units")
async def get_units():
    from backend.db.db_manager import get_table_names  # получение списка таблиЦ
    try:
        units = get_table_names()
        return {"units": units}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving units.")


@router.get("/parameters/{unit}")
async def get_parameters(unit: str):
    from backend.db.db_manager import get_column_names  # получение списка полей таблицЫ
    try:
        parameters = get_column_names(unit)
        return {"parameters": parameters}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving parameters for the selected unit.")


 # – Корневой маршрут –
@router.get("/")
async def root():
    return {"message": "Service is running!"}