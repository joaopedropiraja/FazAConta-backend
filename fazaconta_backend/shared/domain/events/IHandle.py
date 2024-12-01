from abc import ABC, abstractmethod


class IHandle(ABC):
    @abstractmethod
    def setup_subscriptions(self): ...
