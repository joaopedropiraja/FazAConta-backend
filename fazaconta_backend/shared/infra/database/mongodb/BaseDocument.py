from uuid import UUID, uuid4
from pydantic import Field
from beanie import Delete, Document, Insert, Replace, SaveChanges, Update, after_event

from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.domain.events.DomainEvents import DomainEvents


class BaseDocument(Document):
    id: UUID = Field(default_factory=uuid4)

    @after_event(Insert, Replace, Update, Delete, SaveChanges)
    def dispatchEventsCallback(self):
        entityId = UniqueEntityId(self.id)
        DomainEvents.dispatch_events_for_entity(entityId)
