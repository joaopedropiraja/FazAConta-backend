from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument

T = TypeVar("T", bound=Entity)
D = TypeVar("D", bound=BaseDocument)


class Mapper(Generic[T, D], ABC):

    @abstractmethod
    async def to_domain(self, model: D) -> T: ...

    @abstractmethod
    async def to_model(self, entity: T) -> D: ...
