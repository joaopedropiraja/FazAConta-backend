from contextlib import asynccontextmanager

from fastapi import FastAPI
from fazaconta_backend.shared.infra.config.mongo import MongoManager
from fazaconta_backend.shared.infra.config.redis import RedisManager


class App:

    @staticmethod
    def connect():
        app = FastAPI(lifespan=App.lifespan)

        App.set_routes(app)

        return app

    @staticmethod
    def set_routes(app: FastAPI): ...

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.mongo_client = await MongoManager.connect()
        app.state.redis = await RedisManager.connect()

        yield

        await MongoManager.close(app.state.mongo_client)
        await RedisManager.close(app.state.redis)
