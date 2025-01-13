from __future__ import annotations
from abc import ABC, abstractmethod
from fazaconta_backend.modules.group.repos.IGroupRepo import IGroupRepo
from fazaconta_backend.modules.group.repos.IPendingPaymentRepo import (
    IPendingPaymentRepo,
)
from fazaconta_backend.modules.group.repos.ITransactionRepo import (
    ITransactionRepo,
)
from fazaconta_backend.modules.user.repos.IUserRepo import IUserRepo


class AbstractUnitOfWork(ABC):
    users: IUserRepo
    groups: IGroupRepo
    transactions: ITransactionRepo
    pending_payments: IPendingPaymentRepo

    @abstractmethod
    async def __aenter__(self) -> AbstractUnitOfWork: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
