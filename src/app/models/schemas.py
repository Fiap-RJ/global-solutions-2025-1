# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class SensorDataInput(BaseModel):
    """
    Schema para os dados de entrada do sensor.
    Utiliza validação do Pydantic.
    """
    temperature: float = Field(..., gt=-50, lt=100, description="Temperatura em graus Celsius.")
    humidity: float = Field(..., gt=0, le=100, description="Umidade relativa do ar em porcentagem.")
    timestamp: Optional[str] = Field(None, description="Timestamp opcional da medição (formato ISO).")

class RiskPredictionOutput(BaseModel):
    """
    Schema para a resposta da predição de risco.
    """
    timestamp_received: Optional[str]
    input_temperature_c: float
    input_humidity_pct: float
    calculated_heat_index_c: float
    predicted_simplified_risk_label: int
    predicted_simplified_risk_name: str
    alert_message: str

# Você pode adicionar outros schemas aqui conforme necessário
