from __future__ import annotations
from abc import ABC
from fazaconta_backend.modules.group.infra.models.GroupDocument import GroupDocument
from fazaconta_backend.modules.group.infra.models.PendingPaymentDocument import (
    PendingPaymentDocument,
)
from fazaconta_backend.modules.group.infra.models.TransactionDocument import (
    TransactionDocument,
)
from fazaconta_backend.modules.group.mappers.GroupMapper import GroupMapper
from fazaconta_backend.modules.group.mappers.PendingPaymentMapper import (
    PendingPaymentMapper,
)
from fazaconta_backend.modules.group.mappers.TransactionMapper import (
    TransactionMapper,
)
from fazaconta_backend.modules.group.repos.implmentations.MongoGroupRepo import (
    MongoGroupRepo,
)
from fazaconta_backend.modules.group.repos.implmentations.MongoPendingPaymentRepo import (
    MongoPendingPaymentRepo,
)
from fazaconta_backend.modules.group.repos.implmentations.MongoTransactionRepo import (
    MongoTransactionRepo,
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
from fazaconta_backend.modules.group.repos.AbstractTransactionRepo import (
    AbstractTransactionRepo,
)


class MongoUnitOfWork(AbstractUnitOfWork, ABC):
    _client: AsyncIOMotorClient
    _session: AsyncIOMotorClientSession
    users: AbstractUserRepo
    transactions: AbstractTransactionRepo

    def __init__(self, client: AsyncIOMotorClient) -> None:
        self._client = client

    async def __aenter__(self) -> MongoUnitOfWork:
        self._session = await self._client.start_session()
        self._session.start_transaction()

        self.users = MongoUserRepo(UserDocument, UserMapper, self._session)
        self.groups = MongoGroupRepo(GroupDocument, GroupMapper, self._session)
        self.transactions = MongoTransactionRepo(
            TransactionDocument, TransactionMapper, self._session
        )
        self.pending_payments = MongoPendingPaymentRepo(
            PendingPaymentDocument, PendingPaymentMapper, self._session
        )

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self._session.end_session()

    async def commit(self):
        await self._session.commit_transaction()
        return self

    async def rollback(self):
        await self._session.abort_transaction()
