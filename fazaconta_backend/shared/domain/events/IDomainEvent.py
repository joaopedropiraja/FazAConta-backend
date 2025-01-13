from abc import ABC, abstractmethod
import datetime

from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class IDomainEvent(ABC):
    date_time_occurred: datetime.date

    @abstractmethod
    def get_entity_id(self) -> UniqueEntityId: ...
