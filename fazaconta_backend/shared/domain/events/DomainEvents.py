from typing import Callable, Any

from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.domain.events.IDomainEvent import IDomainEvent


class DomainEvents:
    _handlers_map: dict[str, list[Callable[[IDomainEvent], None]]] = {}
    _marked_entities: list[Any] = []

    @staticmethod
    def mark_entity_for_dispatch(entity: Any) -> None:
        if not DomainEvents._find_marked_entity_by_id(entity.id):
            DomainEvents._marked_entities.append(entity)

    @staticmethod
    def dispatch_events_for_entity(id: UniqueEntityId) -> None:
        entity = DomainEvents._find_marked_entity_by_id(id)
        if entity:
            DomainEvents._dispatch_entity_events(entity)
            entity.clear_events()
            DomainEvents._remove_entity_from_marked_dispatch_list(entity)

    @staticmethod
    def register(
        callback: Callable[[IDomainEvent], None], event_class_name: str
    ) -> None:
        if event_class_name not in DomainEvents._handlers_map:
            DomainEvents._handlers_map[event_class_name] = []
        DomainEvents._handlers_map[event_class_name].append(callback)

    @staticmethod
    def clear_handlers() -> None:
        DomainEvents._handlers_map.clear()

    @staticmethod
    def clear_marked_entities() -> None:
        DomainEvents._marked_entities.clear()

    @staticmethod
    def _dispatch_entity_events(entity: Any) -> None:
        for event in entity.domain_events:
            DomainEvents._dispatch(event)

    @staticmethod
    def _remove_entity_from_marked_dispatch_list(entity: Any) -> None:
        DomainEvents._marked_entities = [
            a for a in DomainEvents._marked_entities if not a.equals(entity)
        ]

    @staticmethod
    def _find_marked_entity_by_id(id: UniqueEntityId) -> Any | None:
        for entity in DomainEvents._marked_entities:
            if entity.id == id:
                return entity

        return None

    @staticmethod
    def _dispatch(event: IDomainEvent) -> None:
        event_class_name = event.__class__.__name__
        if event_class_name in DomainEvents._handlers_map:
            for handler in DomainEvents._handlers_map[event_class_name]:
                handler(event)
