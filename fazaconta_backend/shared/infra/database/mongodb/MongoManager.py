from beanie import init_beanie
from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.shared.infra.config.logger import logger
from motor.motor_asyncio import AsyncIOMotorClient

from fazaconta_backend.shared.infra.config.settings import Settings


class MongoManager:

    @staticmethod
    async def connect() -> AsyncIOMotorClient:
        client = AsyncIOMotorClient(Settings().MONGO_URI)
        await init_beanie(
            database=client[Settings().DATABASE_NAME],
            document_models=[UserDocument],
        )
        logger.info("✅ Established connection with mongodb")

        return client

    @staticmethod
    async def close(client: AsyncIOMotorClient):
        client.close()
