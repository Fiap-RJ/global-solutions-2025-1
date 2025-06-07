# /data_generator/src/simulation.py

import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from .utils import assign_risk_label, calculate_heat_index


def generate_simulation_data(num_samples: int) -> pd.DataFrame:
    """Gera o DataFrame com os dados simulados."""
    data = []
    current_time = datetime.now()

    for i in range(num_samples):
        if i < num_samples * 0.3:
            temp_c, hum_pct = np.random.uniform(20, 30), np.random.uniform(40, 70)
        elif i < num_samples * 0.6:
            temp_c, hum_pct = np.random.uniform(28, 35), np.random.uniform(50, 80)
        elif i < num_samples * 0.85:
            temp_c, hum_pct = np.random.uniform(32, 38), np.random.uniform(60, 90)
        else:
            temp_c, hum_pct = np.random.uniform(35, 42), np.random.uniform(70, 95)

        # Adiciona ruído aleatório para simular variações naturais
        temp_c = np.clip(temp_c + np.random.normal(0, 1.5), 15, 45)
        hum_pct = np.clip(hum_pct + np.random.normal(0, 5), 10, 100)

        ic = calculate_heat_index(temp_c, hum_pct)
        label = assign_risk_label(ic)

        data.append([current_time.isoformat(), temp_c, hum_pct, ic, label])
        current_time += timedelta(minutes=np.random.randint(5, 15))

    df = pd.DataFrame(
        data,
        columns=[
            "timestamp",
            "temperature_c",
            "humidity_pct",
            "heat_index_c",
            "risk_label",
        ],
    )
    return df.sample(frac=1).reset_index(drop=True)


def save_data_to_csv(df: pd.DataFrame, path: str, filename: str):
    """Salva o DataFrame em um arquivo CSV."""
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = os.path.join(path, filename)
    df.to_csv(full_path, index=False)
    print(f"Dados salvos com sucesso em: {full_path}")
