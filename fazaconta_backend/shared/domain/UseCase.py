from typing import Generic, TypeVar
from abc import ABC, abstractmethod

IRequest = TypeVar("IRequest")
IResponse = TypeVar("IResponse")


class IUseCase(Generic[IRequest, IResponse], ABC):
    @abstractmethod
    async def execute(self, request: IRequest) -> IResponse: ...
