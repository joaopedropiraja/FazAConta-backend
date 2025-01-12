from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from fazaconta_backend.modules.user.infra.routes.user import users_router
from fazaconta_backend.modules.user.infra.routes.session import sessions_router
from fazaconta_backend.modules.group.infra.routes.group import (
    groups_router,
)
from fazaconta_backend.modules.group.infra.routes.transference import (
    transferences_router,
)
from fazaconta_backend.modules.user.services.implementations.RedisAuthService import (
    RedisAuthService,
)
from fazaconta_backend.modules.user.subscriptions import init_user_handlers
from fazaconta_backend.shared.application.exceptions import ApplicationException
from fazaconta_backend.shared.domain.Guard import GuardException
from fazaconta_backend.shared.domain.exceptions import DomainException
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


class MyAPIApp:

    def __init__(self):
        self.__app = FastAPI(
            title="FazAConta", version=Settings().APP_VERSION, lifespan=self._lifespan
        )

        self._set_middlewares()

        self._set_routers()

        self._set_exception_handlers()

    @property
    def app(self) -> FastAPI:
        return self.__app

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI) -> AsyncGenerator:
        mongo_client = await MongoManager.connect()
        redis = await RedisManager.connect()
        file_handler = (
            LocalFileHandler() if Settings().ENV == "development" else S3FileHandler()
        )
        uow = MongoUnitOfWork(mongo_client)
        auth_service = RedisAuthService(redis)

        # init_user_handlers(uow)

        yield {
            "mongo_client": mongo_client,
            "redis_client": redis,
            "uow": uow,
            "file_handler": file_handler,
            "auth_service": auth_service,
        }

        await MongoManager.close(mongo_client)
        await RedisManager.close(redis)

    def _set_middlewares(self) -> None:
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _set_routers(self) -> None:
        self.__app.include_router(users_router)
        self.__app.include_router(sessions_router)
        self.__app.include_router(groups_router)
        self.__app.include_router(transferences_router)

        if Settings().ENV == "development":
            # Disponibiliza os arquivos salvos na pasta "/temp"
            os.makedirs(Settings().FILES_PATH, exist_ok=True)
            self.__app.mount(
                "/files", StaticFiles(directory=Settings().FILES_PATH), name="files"
            )

    def _set_exception_handlers(self) -> None:
        @self.__app.exception_handler(RequestValidationError)
        async def validation_exception_handler(
            request: Request, exc: RequestValidationError
        ):
            errors = []
            for err in exc.errors():
                loc = err.get("loc", [])
                msg = err.get("msg", "")
                err_type = err.get("type", "")
                errors.append(
                    {
                        "field": ".".join(str(x) for x in loc),
                        "message": msg,
                        "error_type": err_type,
                    }
                )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": errors,
                },
            )

        @self.__app.exception_handler(GuardException)
        async def guard_exception_handler(request: Request, exc: GuardException):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": str(exc),
                },
            )

        @self.__app.exception_handler(DomainException)
        async def domain_exception_handler(request: Request, exc: DomainException):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": str(exc),
                },
            )

        @self.__app.exception_handler(ApplicationException)
        async def application_exception_handler(
            request: Request, exc: ApplicationException
        ):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": str(exc),
                },
            )

        @self.__app.exception_handler(ValidationError)
        async def pydantic_validation_exception_handler(
            request: Request, exc: ValidationError
        ):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": exc.errors(),
                },
            )

        @self.__app.exception_handler(Exception)
        async def internal_exception_handler(request: Request, exc: Exception):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "Internal server error",
                    "errors": str(exc),
                },
            )
