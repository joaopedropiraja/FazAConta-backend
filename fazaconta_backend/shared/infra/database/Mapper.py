from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument

T = TypeVar("T", bound=Entity)
D = TypeVar("D", bound=BaseDocument)


class Mapper(Generic[T, D], ABC):

    @staticmethod
    @abstractmethod
    async def to_domain(model: D) -> T: ...

    @staticmethod
    @abstractmethod
    async def to_model(entity: T) -> D: ...

    @staticmethod
    @abstractmethod
    def to_dto(entity: T) -> Any: ...
