# app/services/climate_service.py
import joblib
import pandas as pd
from pathlib import Path

# --- Configuração do Caminho do Modelo ---
# Assume que a pasta 'ml_models' está um nível acima da pasta 'app'
# Ex: climate_risk_api/ml_models/ e climate_risk_api/app/
BASE_DIR = Path(__file__).resolve().parent.parent.parent # Raiz do projeto (climate_risk_api)
MODEL_PATH = BASE_DIR / "ml_models" / "climate_risk_classifier_model.pkl"

# --- Carregamento do Modelo ---
try:
    model = joblib.load(MODEL_PATH)
    print(f"Modelo de Machine Learning carregado com sucesso de: {MODEL_PATH}")
except FileNotFoundError:
    print(f"ERRO CRÍTICO: O arquivo do modelo não foi encontrado em {MODEL_PATH}.")
    print("Certifique-se de que o modelo foi treinado e está no local correto.")
    model = None
except Exception as e:
    print(f"Ocorreu um erro inesperado ao carregar o modelo: {e}")
    model = None

# --- Mapeamento de Risco ---
simplified_risk_map = {
    0: "Baixo/Normal (IC <= 36°C)",
    1: "Moderado (36°C < IC <= 40°C)",
    2: "Alto (40°C < IC <= 44°C)",
    3: "Muito Alto/Extremo (IC > 44°C)"
}

# --- Funções de Serviço ---
def calculate_heat_index_service(temp_celsius: float, relative_humidity_percent: float) -> float:
    """
    Calcula o Índice de Calor (Heat Index) usando a fórmula da NOAA.
    """
    temp_fahrenheit = (temp_celsius * 9/5) + 32
    rh = relative_humidity_percent

    hi_fahrenheit = -42.379 + (2.04901523 * temp_fahrenheit) + \
                    (10.14333127 * rh) - \
                    (0.22475541 * temp_fahrenheit * rh) - \
                    (0.00683783 * temp_fahrenheit**2) - \
                    (0.05481717 * rh**2) + \
                    (0.00122874 * temp_fahrenheit**2 * rh) + \
                    (0.00085282 * temp_fahrenheit * rh**2) - \
                    (0.00000199 * temp_fahrenheit**2 * rh**2)

    if rh < 13 and (80 <= temp_fahrenheit <= 112):
        adjustment = ((13 - rh) / 4) * (((17 - abs(temp_fahrenheit - 95)) / 17)**0.5)
        hi_fahrenheit -= adjustment
    
    if rh > 85 and (80 <= temp_fahrenheit <= 87):
        adjustment = ((rh - 85) / 10) * ((87 - temp_fahrenheit) / 5)
        hi_fahrenheit += adjustment

    if hi_fahrenheit < 80:
        hi_fahrenheit = temp_fahrenheit

    hi_celsius = (hi_fahrenheit - 32) * 5/9
    return hi_celsius

def predict_risk_service(temperature_c: float, humidity_pct: float) -> tuple[int, str]:
    """
    Utiliza o modelo de ML carregado para prever o risco.
    Retorna o label numérico do risco e o nome descritivo do risco.
    Levanta uma exceção se o modelo não estiver carregado.
    """
    if not model:
        raise ValueError("Modelo de Machine Learning não está carregado ou falhou ao carregar.")

    # Preparar os dados para o modelo
    features_df = pd.DataFrame([[temperature_c, humidity_pct]], columns=['temperature_c', 'humidity_pct'])
    
    # Fazer a predição
    prediction_result = model.predict(features_df)
    predicted_label = int(prediction_result[0])
    
    predicted_risk_name = simplified_risk_map.get(predicted_label, "Risco Desconhecido")
    
    return predicted_label, predicted_risk_name