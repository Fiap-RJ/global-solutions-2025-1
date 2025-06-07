import pandas as pd
from utils.utils import RISK_MAP


class ClimateService:
    def __init__(self, repository, model):
        self.repository = repository
        self.model = model

    def calculate_heat_index(
        self, temp_celsius: float, relative_humidity_percent: float
    ) -> float:
        """
        Calcula o índice de calor (heat index) com base na temperatura e umidade.
        """
        temp_fahrenheit = (temp_celsius * 9 / 5) + 32
        rh = relative_humidity_percent

        hi_fahrenheit = (
            -42.379
            + (2.04901523 * temp_fahrenheit)
            + (10.14333127 * rh)
            - (0.22475541 * temp_fahrenheit * rh)
            - (0.00683783 * temp_fahrenheit**2)
            - (0.05481717 * rh**2)
            + (0.00122874 * temp_fahrenheit**2 * rh)
            + (0.00085282 * temp_fahrenheit * rh**2)
            - (0.00000199 * temp_fahrenheit**2 * rh**2)
        )

        if rh < 13 and (80 <= temp_fahrenheit <= 112):
            adjustment = ((13 - rh) / 4) * (
                ((17 - abs(temp_fahrenheit - 95)) / 17) ** 0.5
            )
            hi_fahrenheit -= adjustment

        if rh > 85 and (80 <= temp_fahrenheit <= 87):
            adjustment = ((rh - 85) / 10) * ((87 - temp_fahrenheit) / 5)
            hi_fahrenheit += adjustment

        if hi_fahrenheit < 80:
            hi_fahrenheit = temp_fahrenheit

        hi_celsius = (hi_fahrenheit - 32) * 5 / 9
        return hi_celsius

    def predict_risk(
        self, temperature_c: float, humidity_pct: float
    ) -> tuple[int, str]:
        """
        Usa o modelo injetado para prever o risco e salva no repositório.
        """
        if not self.model:
            raise ValueError("Model is not loaded or available.")

        features_df = pd.DataFrame(
            [[temperature_c, humidity_pct]], columns=["temperature_c", "humidity_pct"]
        )

        predicted_label = int(self.model.predict(features_df)[0])
        predicted_risk_name = RISK_MAP.get(predicted_label, "Risco Desconhecido")

        self.repository.save_prediction(
            {
                "temperature_c": temperature_c,
                "humidity_pct": humidity_pct,
                "risk_label": predicted_label,
                "risk_name": predicted_risk_name,
            }
        )

        return predicted_label, predicted_risk_name
