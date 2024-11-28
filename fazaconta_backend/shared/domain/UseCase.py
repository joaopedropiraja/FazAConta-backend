from typing import Generic, TypeVar, Awaitable
from abc import ABC, abstractmethod

IRequest = TypeVar("IRequest")
IResponse = TypeVar("IResponse")


class IUseCase(Generic[IRequest, IResponse], ABC):
    @abstractmethod
    def execute(self, request: IRequest) -> Awaitable[IResponse] | IResponse: ...
