from abc import ABC
from typing import Type, TypeVar, Generic, Optional, List

from fazaconta_backend.shared.domain.AbstractGenericRepository import (
    AbstractGenericRepository,
)
from motor.motor_asyncio import AsyncIOMotorClientSession
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.infra.database.Mapper import Mapper
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument

T = TypeVar("T", bound=Entity)
D = TypeVar("D", bound=BaseDocument)


class GenericMongoRepository(Generic[T, D], AbstractGenericRepository[T], ABC):

    def __init__(
        self,
        model_cls: Type[D],
        mapper: Mapper[T, D],
        session: AsyncIOMotorClientSession | None,
    ):
        self._model_cls = model_cls
        self._mapper = mapper
        self._session = session

    async def get_by_id(self, id: str) -> Optional[T]:
        doc = await self._model_cls.get(id)
        return await self._mapper.to_domain(doc) if doc else None

    async def find(self, **filters) -> T | None:
        doc = await self._model_cls.find_one(filters)
        return await self._mapper.to_domain(doc) if doc else None

    async def list(self, **filters) -> List[T]:
        query = self._model_cls.find(filters)
        docs = await query.to_list()
        return [await self._mapper.to_domain(doc) for doc in docs]

    async def add(self, entity: T) -> T:
        doc = await self._mapper.to_model(entity)
        createdDoc = await doc.insert(session=self._session)
        return await self._mapper.to_domain(createdDoc)

    async def update(self, entity: T) -> T:
        doc = await self._mapper.to_model(entity)
        updatedDoc = await doc.save(session=self._session)
        return await self._mapper.to_domain(updatedDoc)

    async def delete(self, id: str) -> None:
        document = await self._model_cls.get(id)
        if document:
            await document.delete(session=self._session)
