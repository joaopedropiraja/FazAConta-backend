from abc import ABC
import datetime

from UniqueEntityId import UniqueEntityId


class IDomainEvent(ABC):
    dateTimeOccurred: datetime.date

    def getAggregateId(self) -> UniqueEntityId: ...
