from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fazaconta_backend.modules.user.infra.routes import users_router
from fazaconta_backend.modules.user.subscriptions import init_user_handlers
from fazaconta_backend.shared.domain.files.CloudUpload import CloudUpload
from fazaconta_backend.shared.infra.config.settings import Settings
from fazaconta_backend.shared.infra.database.mongodb.MongoManager import MongoManager
from fazaconta_backend.shared.infra.config.redis import RedisManager
from fazaconta_backend.shared.infra.database.mongodb.MongoUnitOfWork import (
    MongoUnitOfWork,
)
from fazaconta_backend.shared.infra.services.files.LocalFileHandler import (
    LocalFileHandler,
)
from fazaconta_backend.shared.infra.services.files.S3FileHandler import S3FileHandler


class App:

    @staticmethod
    def connect():
        app = FastAPI(lifespan=App.lifespan)

        App.set_routes(app)

        return app

    @staticmethod
    def set_routes(app: FastAPI):
        app.include_router(users_router)

        if Settings().ENV == "develoment":
            os.makedirs(Settings().FILES_PATH, exist_ok=True)
            app.mount(
                "/files", StaticFiles(directory=Settings().FILES_PATH), name="files"
            )

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        mongo_client = await MongoManager.connect()
        redis = await RedisManager.connect()
        file_handler = (
            LocalFileHandler() if Settings().ENV == "development" else S3FileHandler()
        )
        uow = MongoUnitOfWork(mongo_client)

        init_user_handlers(uow)

        yield {
            "mongo_client": mongo_client,
            "redis_client": redis,
            "uow": uow,
            "file_handler": file_handler,
        }

        await MongoManager.close(mongo_client)
        await RedisManager.close(redis)
