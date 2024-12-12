from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Identifier(Generic[T], ABC):
    value: T

    def __str__(self) -> str:
        return str(self.value)
