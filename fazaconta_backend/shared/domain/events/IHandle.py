from abc import ABC, abstractmethod


class IHandle(ABC):
    @abstractmethod
    def setupSubscriptions(self): ...
