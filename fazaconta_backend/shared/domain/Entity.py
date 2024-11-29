from __future__ import annotations
from abc import ABC
from ast import TypeVar
from fazaconta_backend.shared.domain.BusinessRuleValidationMixin import (
    BusinessRuleValidationMixin,
)
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.domain.events.DomainEvents import DomainEvents
from fazaconta_backend.shared.domain.events.IDomainEvent import IDomainEvent
from pydantic import BaseModel

T = TypeVar("T")


class Entity(ABC, BaseModel, BusinessRuleValidationMixin):
    id: UniqueEntityId = UniqueEntityId()
    _domain_events: list[IDomainEvent] = []

    def equals(self, obj: Entity):
        if obj is None or not isinstance(obj, Entity):
            return false

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
        print(f"[Domain Event Created]: {aggregate_class_name} ==> {event_class_name}")
