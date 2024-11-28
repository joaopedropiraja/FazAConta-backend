from __future__ import annotations
from abc import ABC
from ast import TypeVar
from dataclasses import dataclass
from UniqueEntityId import UniqueEntityId
from BusinessRuleValidationMixin import BusinessRuleValidationMixin
from pydantic import BaseModel


T = TypeVar("T")


class Entity(ABC, BaseModel, BusinessRuleValidationMixin):
    id: UniqueEntityId = UniqueEntityId()

    def equals(self, obj: Entity):
        if obj is None or not isinstance(obj, Entity):
            return false

        return self.id == obj.id


obj = Entity()

print(obj.id)
