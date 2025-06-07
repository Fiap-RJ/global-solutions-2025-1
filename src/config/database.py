from pymongo import MongoClient
import os
from config.config import settings


def get_database():
    """
    Cria e retorna a conexão com o banco de dados MongoDB.
    """
    client = MongoClient(settings.MONGO_CONNECTION_STRING)
    return client[settings.MONGO_DATABASE_NAME]
