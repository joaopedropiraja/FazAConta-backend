from abc import ABC, abstractmethod
import datetime

from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class IDomainEvent(ABC):
    dateTimeOccurred: datetime.date

    @abstractmethod
    def getEntityId(self) -> UniqueEntityId: ...
