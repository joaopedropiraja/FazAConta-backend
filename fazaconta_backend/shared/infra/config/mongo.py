from contextlib import asynccontextmanager
from beanie import init_beanie
from fazaconta_backend.shared.infra.config.logger import logger
from motor.motor_asyncio import AsyncIOMotorClient

from fazaconta_backend.shared.infra.config.settings import Settings


class MongoManager:

    @staticmethod
    async def connect() -> AsyncIOMotorClient:
        client = AsyncIOMotorClient(Settings().mongo_uri)
        await init_beanie(
            database=client[Settings().database_name],
            document_models=[],
        )
        logger.info("✅ Established connection with mongodb")

        return client

    @staticmethod
    async def close(client: AsyncIOMotorClient):
        client.close()
