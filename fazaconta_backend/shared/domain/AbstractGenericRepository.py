from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


T = TypeVar("T", bound=Entity)


class AbstractGenericRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> T | None: ...

    @abstractmethod
    async def get_one(self, **filters) -> T | None: ...

    @abstractmethod
    async def get(self, limit: int, skip: int, **filters) -> list[T]: ...

    @abstractmethod
    async def create(self, entity: T) -> T: ...

    @abstractmethod
    async def update(self, entity: T) -> T: ...

    @abstractmethod
    async def delete(self, id: UniqueEntityId) -> None: ...
