# /model_trainer/src/model.py

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
import joblib
import os


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Cria e treina um modelo RandomForestClassifier."""
    print("Iniciando o treinamento do modelo...")

    model = RandomForestClassifier(
        random_state=42, n_estimators=100, max_depth=10, class_weight="balanced"
    )
    model.fit(X_train, y_train)

    return model


def evaluate_model(
    model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series
):
    """Avalia o desempenho do modelo no conjunto de teste."""
    print("\n--- Avaliação do Modelo ---")

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do Modelo: {accuracy:.4f}")

    print("\nRelatório de Classificação:")
    target_names = ["Baixo/Normal", "Moderado", "Alto", "Muito Alto/Extremo"]
    print(
        classification_report(
            y_test, y_pred, target_names=target_names, zero_division=0
        )
    )

    print("\nMatriz de Confusão:")
    print(confusion_matrix(y_test, y_pred))


def save_model(model: RandomForestClassifier, path: str, filename: str):
    """Salva o modelo treinado em um arquivo .pkl."""
    if not os.path.exists(path):
        os.makedirs(path)

    full_path = os.path.join(path, filename)
    joblib.dump(model, full_path)
    print(f"\nModelo salvo com sucesso em: {full_path}")
