from datetime import datetime

from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.domain.events.IDomainEvent import IDomainEvent


class UserCreated(IDomainEvent):
    def __init__(self, userId: UniqueEntityId) -> None:

        self.date_time_occurred = datetime.now()
        self.userId = userId

    def get_entity_id(self) -> UniqueEntityId:

        return self.userId
