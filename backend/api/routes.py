import threading

from fastapi import APIRouter, HTTPException

from backend.data.generator import main as generator_main, stop_generator
from backend.db.db_manager import get_data_from_table

router = APIRouter()
generator_thread = None
generator_running = False


def generator_wrapper():
    global generator_running
    generator_running = True
    try:
        generator_main()  # Запуск основного генератора
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
        stop_generator()  # Останавливаем генератор
        generator_thread.join()  # Ждём завершения потока
        generator_running = False
        return {"status": "Generator stopped"}
    else:
        return {"status": "Generator is not running"}


@router.get("/data/{table_name}")
async def get_sensor_data(table_name: str):
    try:
        data = get_data_from_table(table_name)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def root():
    return {"message": "Service is running!"}