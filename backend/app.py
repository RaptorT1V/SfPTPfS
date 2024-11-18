from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../backend/logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Service for Plotting Technical Parameters from Sensors",
    description="Сервис для построения графиков технических параметров с датчиков"
)

BASE_DIR = Path(__file__).resolve().parent

# Папка для графиков (если ещё не создана)
plot_dir = BASE_DIR / "graphics"
if not plot_dir.exists():
    plot_dir.mkdir(parents=True, exist_ok=True)
logger.info(f"[app.py]; Plot directory --> {plot_dir.resolve()}")

# Монтируем статические файлы
app.mount("/graphics", StaticFiles(directory=BASE_DIR / "graphics"), name="backend-graphics")
app.mount("/static", StaticFiles(directory=BASE_DIR.parent / "web" / "static"), name="web-static")

logger.info("[app.py]; Static file routes mounted.")

app.include_router(router)
logger.info("[app.py]; Router included.")

if __name__ == "__main__":
    import uvicorn
    logger.info("[app.py]; Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)