from __future__ import annotations
from abc import ABC, abstractmethod
from fazaconta_backend.modules.group.repos.AbstractGroupRepo import AbstractGroupRepo
from fazaconta_backend.modules.group.repos.AbstractPendingPaymentRepo import (
    AbstractPendingPaymentRepo,
)
from fazaconta_backend.modules.group.repos.AbstractTransactionRepo import (
    AbstractTransactionRepo,
)
from fazaconta_backend.modules.user.repos.AbstractUserRepo import AbstractUserRepo


class AbstractUnitOfWork(ABC):
    users: AbstractUserRepo
    groups: AbstractGroupRepo
    transactions: AbstractTransactionRepo
    pending_payments: AbstractPendingPaymentRepo

    @abstractmethod
    async def __aenter__(self) -> AbstractUnitOfWork: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
