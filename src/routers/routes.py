# src/routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated
from models.schemas import RiskPredictionOutput, SensorDataInput
from services.climate_service import ClimateService
from utils.logger import logger

router = APIRouter(
    prefix="/api/v1",
    tags=["Climate Risk Prediction"],
)


def get_climate_service(request: Request):
    """
    Dependency to get the climate service instance.
    This can be used to inject the service into endpoints.
    """
    return request.state.climate_service


@router.post(
    "/predict",
    response_model=RiskPredictionOutput,
    summary="Prever Risco Climático",
    description="Recebe dados de temperatura e umidade, calcula o Índice de Calor e prevê o nível de risco instantâneo.",
)
def predict_climate_risk(
    climate_service: Annotated[ClimateService, Depends(get_climate_service)],
    data: SensorDataInput,
):
    """
    Endpoint para predição de risco climático.
    Recebe os dados do sensor, processa e retorna a predição.
    """
    try:
        current_ic = climate_service.calculate_heat_index(
            data.temperature, data.humidity
        )

        predicted_label, predicted_risk_name = climate_service.predict_risk(
            data.temperature, data.humidity
        )

        alert_message = f"Risco instantâneo detectado: {predicted_risk_name}."

        response = RiskPredictionOutput(
            timestamp_received=data.timestamp,
            input_temperature_c=data.temperature,
            input_humidity_pct=data.humidity,
            calculated_heat_index_c=round(current_ic, 2),
            predicted_risk_label=predicted_label,
            predicted_risk_name=predicted_risk_name,
            alert_message=alert_message,
        )

        logger.info(
            "[Router] Response: Temp=%s°C, Hum=%s%% -> IC=%.2f°C -> Risco=%s",
            data.temperature,
            data.humidity,
            current_ic,
            predicted_risk_name,
        )

        return response

    except ValueError as e:
        logger.error("[Router] Error in prediction: %s", str(e))
        raise HTTPException(status_code=500, detail=str(ve)) from e
