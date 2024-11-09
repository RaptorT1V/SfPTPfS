from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router
import logging

logging.basicConfig(
    level=logging.INFO,  # Используйте DEBUG для более подробных логов
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../backend/logs/app.log"),  # Логи записываются в файл
        logging.StreamHandler()  # Логи также выводятся в консоль
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Service for Plotting Technical Parameters from Sensors",
    description="API для работы с данными и построением графиков для параметров заводских сенсоров"
)

# Получаем абсолютный путь к текущей директории, где находится app.py
BASE_DIR = Path(__file__).resolve().parent

# Создаём директорию для графиков
plot_dir = BASE_DIR / "static/plots"
plot_dir.mkdir(parents=True, exist_ok=True)
logger.info(f"[app.py]; Plot directory set up at {plot_dir.resolve()}")

# Создаём директорию для статических файлов, если её нет
static_backend_path = BASE_DIR / "static"
if not static_backend_path.exists():
    static_backend_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"[app.py]; Static directory created at {static_backend_path.resolve()}")

# Монтируем статические файлы
app.mount("/graphics", StaticFiles(directory=BASE_DIR / "graphics"), name="backend-graphics")
app.mount("/static", StaticFiles(directory=BASE_DIR.parent / "web" / "static"), name="web-static")

logger.info("[app.py]; Static file routes mounted.")

# Подключение маршрутов
app.include_router(router)
logger.info("[app.py]; Router included.")

if __name__ == "__main__":
    import uvicorn
    logger.info("[app.py]; Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)