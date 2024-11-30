import redis.asyncio as redis
from fazaconta_backend.shared.infra.config.logger import logger

from fazaconta_backend.shared.infra.config.settings import Settings


class RedisManager:

    @staticmethod
    async def connect() -> redis.Redis:
        client = redis.from_url(
            f"redis://{Settings().redis_host}:{Settings().redis_port}?decode_responses=True"
        )
        logger.info("✅ Established connection with redis")

        return client

    @staticmethod
    async def close(client: redis.Redis):
        await client.close()
