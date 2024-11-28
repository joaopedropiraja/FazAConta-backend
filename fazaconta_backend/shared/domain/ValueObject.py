from abc import ABC
from pydantic import BaseModel


class ValueObject(BaseModel, ABC):
    class Config:
        frozen = True
