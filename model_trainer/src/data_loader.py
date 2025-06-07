# /model_trainer/src/data_loader.py

import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple


def load_data(filepath: str) -> pd.DataFrame:
    """Carrega os dados de um arquivo CSV."""
    try:
        df = pd.read_csv(filepath)
        print(f"Dados carregados com sucesso de {filepath}")
        return df
    except FileNotFoundError:
        print(f"Erro: O arquivo de dados não foi encontrado em {filepath}")
        raise


def split_data(
    df: pd.DataFrame, features: list, target: str, test_size: float, random_state: int
) -> Tuple:
    """Divide os dados em conjuntos de treino e teste."""
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,  # Mantém a proporção de classes no split
    )

    print("Dados divididos em conjuntos de treino e teste.")
    return X_train, X_test, y_train, y_test
