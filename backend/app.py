from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(
    title="Service for Plotting Technical Parameters from Sensors",
    description="API для работы с данными и построением графиков для параметров заводских сенсоров"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
