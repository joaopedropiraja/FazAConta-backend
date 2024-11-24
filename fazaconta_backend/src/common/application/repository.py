from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Set
from uuid import UUID

from fazaconta_backend.src.common.domain.entity import Entity as DomainEntity


Entity = TypeVar("Entity", bound=DomainEntity)


class AbstractGenericRepository(Generic[Entity], ABC):
    def __init__(self):
        self.seen = set()

    def list(self, **filters) -> list[Entity]:
        entities = self._list(**filters)
        if len(entities) > 0:
            self.seen.update(entities)

        return entities

    def get_id(self, id: UUID) -> Entity:
        entity = self._get_by_id(id)

        if entity:
            self.seen.add(entity)

        return entity

    def add(self, entity: Entity) -> None:
        self._add(entity)
        self.seen.add(entity)

    def remove(self, entity: Entity) -> None:
        self._remove(entity)
        self.seen.add(entity)

    @abstractmethod
    def _list(self, **filters) -> list[Entity]: ...

    @abstractmethod
    def _get_by_id(self, id: UUID) -> Entity: ...

    @abstractmethod
    def _add(self, entity: Entity): ...

    @abstractmethod
    def _remove(self, id: UUID) -> Entity: ...
