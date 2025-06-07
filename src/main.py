# app/main.py
import datetime
import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI

from config.database import get_database
from repositories.climate_risk_repository import ClimateRiskRepository
from routers import routes as api_routes
from services.climate_service import ClimateService
from utils.logger import logger


MODEL_PATH = os.path.join(
    Path(__file__).resolve().parent, "ml_models", "climate_risk_classifier_model.pkl"
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"[Lifespan] Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        logger.error(f"[Lifespan] Error loading model: {e}")
        model = None

    db = get_database()
    repository = ClimateRiskRepository(db)
    climate_service = ClimateService(repository=repository, model=model)

    yield {
        "climate_service": climate_service,
    }


app = FastAPI(
    title="API de Análise de Risco Climático",
    description="""Uma API que utiliza um modelo de Machine Learning para 
    prever o risco climático instantâneo com base na temperatura e umidade.""",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_routes.router)


@app.get("/health", summary="Health Check")
def health_check():
    """
    Endpoint de verificação de saúde da API.
    Retorna um status de operação da API.
    """
    timestamp = datetime.datetime.now().isoformat()
    return {"status": "healthy", "timestamp": timestamp, "version": app.version}
