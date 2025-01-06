from __future__ import annotations
from abc import ABC
from ast import TypeVar

from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.domain.events.DomainEvents import DomainEvents
from fazaconta_backend.shared.domain.events.IDomainEvent import IDomainEvent
from fazaconta_backend.shared.infra.config.logger import logger


T = TypeVar("T")


class Entity(ABC):
    id: UniqueEntityId = UniqueEntityId()
    _domain_events: list[IDomainEvent] = []

    def __init__(self, id: UniqueEntityId | None) -> None:
        self.id = id if id is not None else UniqueEntityId()

    def equals(self, obj: Entity):
        if obj is None or not isinstance(obj, Entity):
            return False

        return self.id == obj.id

    @property
    def domain_events(self) -> list[IDomainEvent]:
        return self._domain_events

    def add_domain_event(self, domain_event: IDomainEvent) -> None:
        self._domain_events.append(domain_event)
        DomainEvents.mark_entity_for_dispatch(self)
        self._log_domain_event_added(domain_event)

    def clear_events(self) -> None:
        self._domain_events.clear()

    def _log_domain_event_added(self, domain_event: IDomainEvent) -> None:
        aggregate_class_name = self.__class__.__name__
        event_class_name = domain_event.__class__.__name__

        logger.info(
            f"[Domain Event Created]: {aggregate_class_name} ==> {event_class_name}"
        )
