# app/api/routes.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import SensorDataInput, RiskPredictionOutput
from app.services import climate_service  # Importa o módulo de serviço

# Cria um APIRouter. Todos os endpoints definidos aqui serão prefixados
# (se um prefixo for definido ao incluir o router na app principal)
router = APIRouter()


@router.post(
    "/predict",
    response_model=RiskPredictionOutput,
    summary="Prever Risco Climático",
    description="Recebe dados de temperatura e umidade, calcula o Índice de Calor e prevê o nível de risco instantâneo.",
    tags=["Predictions"],
)  # Tags para agrupar endpoints na documentação
async def predict_climate_risk(data: SensorDataInput):
    """
    Endpoint para predição de risco climático.
    Recebe os dados do sensor, processa e retorna a predição.
    """
    try:
        # 1. Calcular o Índice de Calor
        current_ic = climate_service.calculate_heat_index_service(
            data.temperature, data.humidity
        )

        # 2. Fazer a predição usando o modelo de ML
        predicted_label, predicted_risk_name = climate_service.predict_risk_service(
            data.temperature, data.humidity
        )

        # 3. Montar a mensagem de alerta
        alert_message = (
            f"Risco instantâneo detectado: {predicted_risk_name}. "
            "(Nota: Para o Nível de Calor (NC) completo do Rio, a análise de duração é necessária.)"
        )

        # 4. Montar a resposta
        response = RiskPredictionOutput(
            timestamp_received=data.timestamp,
            input_temperature_c=data.temperature,
            input_humidity_pct=data.humidity,
            calculated_heat_index_c=round(current_ic, 2),
            predicted_simplified_risk_label=predicted_label,
            predicted_simplified_risk_name=predicted_risk_name,
            alert_message=alert_message,
        )

        print(
            f"PREVISÃO (API): Temp={data.temperature}°C, Hum={data.humidity}% -> IC={current_ic:.2f}°C -> Risco={predicted_risk_name}"
        )
        return response

    except (
        ValueError
    ) as ve:  # Captura erros específicos do serviço, como modelo não carregado
        print(f"ERRO DE VALOR (API): {ve}")
        raise HTTPException(status_code=503, detail=str(ve))  # Service Unavailable
    except Exception as e:
        # Captura exceções genéricas durante o processamento
        print(f"ERRO INESPERADO (API): {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro interno ao processar a requisição: {str(e)}",
        )


# Você pode adicionar outros endpoints aqui conforme necessário.
# Exemplo: um endpoint para verificar a saúde da API ou do modelo.
@router.get("/health", summary="Verificar Saúde da Aplicação", tags=["Utilities"])
async def health_check():
    if climate_service.model is not None:
        return {"status": "ok", "message": "API e Modelo de ML estão operacionais."}
    else:
        return {
            "status": "error",
            "message": "API operacional, mas o Modelo de ML não está carregado.",
        }
