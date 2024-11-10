from fastapi import APIRouter, HTTPException, WebSocket, Query
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse

from backend.data.generator import main as generator_main, stop_generator
from backend.db.db_manager import get_oldest_timestamp, get_newest_timestamp, get_data_from_table
from backend.api.plot_utils import plot_graph

from pathlib import Path
from typing import Optional
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
@router.get("/plot/{unit}/{parameter}")
async def get_plot(unit: str, parameter: str, start_time: str, end_time: str):
    if start_time >= end_time or end_time <= start_time:
        raise HTTPException(status_code=400, detail="Дата начала не может быть позднее даты конца или наоборот.")

    data = get_data_from_table(unit, parameter, start_time, end_time)

    if not data:
        raise HTTPException(status_code=404, detail="Данные за указанный период отсутствуют.")

    plot_path = plot_graph(data, [parameter], unit=unit, parameter=parameter, format="svg")
    return FileResponse(plot_path, media_type="image/svg+xml")

"""
@router.get("/plot/multi/{unit}")
async def get_multi_plot(unit: str,
                         parameters: list,
                         start_time: Optional[str] = None,
                         end_time: Optional[str] = None,
                         format: str = "png"):
    try:
        start_time = start_time or get_oldest_timestamp(unit)
        end_time = end_time or get_newest_timestamp(unit)

        data = get_data_from_table(unit, parameters, start_time, end_time)
        if not data:
            raise HTTPException(status_code=404, detail="No data found for the selected range")

        image_path = plot_graph(data, parameters, format)
        with open(image_path, "rb") as image_file:
            media_type = "image/svg+xml" if format == "svg" else "image/png"
            return StreamingResponse(image_file, media_type=media_type)
    except Exception as e:
        print(f"Error generating plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))
"""

 # – Web –
@router.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = Path(__file__).parent.parent.parent / "web/templates/index.html"
    index_content = index_path.read_text(encoding="utf-8")
    return HTMLResponse(content=index_content, status_code=200)


@router.websocket("/ws/plot/{unit}/{parameter}")
async def websocket_plot(websocket: WebSocket, unit: str, parameter: str):
    await websocket.accept()
    while True:
        data = get_data_from_table(unit, parameter, start_time=get_newest_timestamp(unit))
        await websocket.send_json(data)
        await asyncio.sleep(2)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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
    from backend.db.db_manager import get_table_names  # функция для получения списка таблиц
    try:
        units = get_table_names()
        return {"units": units}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving units.")


@router.get("/parameters/{unit}")
async def get_parameters(unit: str):
    from backend.db.db_manager import get_column_names  # функция для получения списка полей таблицы
    try:
        parameters = get_column_names(unit)
        return {"parameters": parameters}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving parameters for the selected unit.")


 # – Корневой маршрут –
@router.get("/")
async def root():
    return {"message": "Service is running!"}