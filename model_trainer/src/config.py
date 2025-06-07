# /model_trainer/src/config.py

INPUT_DATA_PATH = "../src/data/simulated_climate_risk_data.csv"

MODEL_OUTPUT_PATH = "../src/ml_models"
MODEL_NAME = "climate_risk_classifier_model.pkl"

TEST_SIZE = 0.25
RANDOM_STATE = 42

FEATURES = ["temperature_c", "humidity_pct"]
TARGET = "risk_label"
