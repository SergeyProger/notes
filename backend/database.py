import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import document_models

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")

async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)

    # Передаем список моделей в Beanie
    await init_beanie(
        database=client.app_database,
        document_models=document_models
    )