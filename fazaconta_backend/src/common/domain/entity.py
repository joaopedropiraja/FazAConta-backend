from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from lato import Event
from .domain_event import DomainEvent


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    events: list[Event] = Field(default_factory=list)

    def register_event(self, event: DomainEvent):
        self.events.append(event)

    def collect_events(self):
        events = self.events
        self.events = []
        return events
