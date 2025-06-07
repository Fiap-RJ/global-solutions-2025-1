from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime
from utils.logger import logger
from config.config import settings


class ClimateRiskRepository:
    def __init__(self, db: Database):
        """
        Inicializa o repositório com a instância do banco de dados.

        Args:
            db (Database): Instância do banco de dados Pymongo.
        """
        self.db = db
        self.collection: Collection = self.db[settings.INFERENCE_COLLECTION_NAME]
        logger.info(
            "[ClimateRiskRepository] Repository initialized with collection: %s",
            settings.INFERENCE_COLLECTION_NAME,
        )

    def save_prediction(self, prediction_data: dict):
        """
        Salva o resultado de uma predição no banco de dados.
        Adiciona um timestamp ao registro antes de salvar.

        Args:
            prediction_data (dict): Dicionário com os dados da predição.
        """
        try:
            document_to_save = prediction_data.copy()
            document_to_save["created_at"] = datetime.now()

            result = self.collection.insert_one(document_to_save)

            logger.info("Prediction saved successfully with ID: %s", result.inserted_id)
            return result
        except Exception as e:
            logger.error(f"Error saving prediction: {e}")
