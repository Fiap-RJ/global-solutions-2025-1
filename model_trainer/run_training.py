# /model_trainer/run_training.py

from src.config import (
    INPUT_DATA_PATH,
    MODEL_OUTPUT_PATH,
    MODEL_NAME,
    FEATURES,
    TARGET,
    TEST_SIZE,
    RANDOM_STATE,
)
from src.data_loader import load_data, split_data
from src.model import train_model, evaluate_model, save_model


def main():
    """Função principal para orquestrar o treinamento do modelo."""
    print("--- INICIANDO PROCESSO DE TREINAMENTO DO MODELO ---")

    df = load_data(filepath=INPUT_DATA_PATH)

    X_train, X_test, y_train, y_test = split_data(
        df=df,
        features=FEATURES,
        target=TARGET,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    trained_model = train_model(X_train=X_train, y_train=y_train)

    evaluate_model(model=trained_model, X_test=X_test, y_test=y_test)

    save_model(model=trained_model, path=MODEL_OUTPUT_PATH, filename=MODEL_NAME)

    print("\n--- PROCESSO DE TREINAMENTO FINALIZADO ---")


if __name__ == "__main__":
    main()
