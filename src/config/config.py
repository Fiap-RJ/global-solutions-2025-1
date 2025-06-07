from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    """
    Carrega as configurações da aplicação.
    """

    MONGO_CONNECTION_STRING: str = "mongodb://localhost:27017/"
    MONGO_DATABASE_NAME: str = "climate_risk_db"
    INFERENCE_COLLECTION_NAME: str = "inferences"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
