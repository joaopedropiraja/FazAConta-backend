from __future__ import annotations
from abc import ABC, abstractmethod


from fazaconta_backend.modules.transference.repos.AbstractTransferenceRepo import (
    AbstractTransferenceRepo,
)
from fazaconta_backend.modules.user.repos.AbstractUserRepo import AbstractUserRepo


class AbstractUnitOfWork(ABC):
    users: AbstractUserRepo
    transferences: AbstractTransferenceRepo

    @abstractmethod
    async def __aenter__(self) -> AbstractUnitOfWork: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
