from __future__ import annotations
from abc import ABC
from fazaconta_backend.modules.group.infra.models.TransferenceDocument import (
    TransferenceDocument,
)
from fazaconta_backend.modules.group.mappers.TransferenceMapper import (
    TransferenceMapper,
)
from fazaconta_backend.modules.group.repos.implmentations.MongoTransferenceRepo import (
    MongoTransferenceRepo,
)
from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.modules.user.repos.implementations.MongoUserRepo import (
    MongoUserRepo,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession


from fazaconta_backend.modules.user.repos.AbstractUserRepo import AbstractUserRepo
from fazaconta_backend.modules.group.repos.AbstractTransferenceRepo import (
    AbstractTransferenceRepo,
)


class MongoUnitOfWork(AbstractUnitOfWork, ABC):
    _client: AsyncIOMotorClient
    _session: AsyncIOMotorClientSession
    users: AbstractUserRepo
    transferences: AbstractTransferenceRepo

    def __init__(self, client: AsyncIOMotorClient) -> None:
        self._client = client

    async def __aenter__(self) -> MongoUnitOfWork:
        self._session = await self._client.start_session()
        self._session.start_transaction()

        self.users = MongoUserRepo(UserDocument, UserMapper, self._session)
        self.transferences = MongoTransferenceRepo(
            TransferenceDocument, TransferenceMapper, self._session
        )

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            await self._session.end_session()

    async def commit(self):
        await self._session.commit_transaction()
        return self

    async def rollback(self):
        await self._session.abort_transaction()
