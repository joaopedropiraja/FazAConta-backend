from abc import ABC, abstractmethod
from pydantic import BaseModel


class BusinessRule(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True

    message: str = "Business rule is broken"

    @abstractmethod
    def is_broken(self) -> bool: ...

    def __str__(self):
        return f"{self.__class__.__name__} {super().__str__()}"
