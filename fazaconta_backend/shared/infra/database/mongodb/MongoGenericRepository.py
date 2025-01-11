from abc import ABC
from typing import Type, TypeVar, Generic, Optional, List

from beanie import DeleteRules, WriteRules

from fazaconta_backend.shared.domain.AbstractGenericRepository import (
    AbstractGenericRepository,
)
from motor.motor_asyncio import AsyncIOMotorClientSession
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument

T = TypeVar("T", bound=Entity)
D = TypeVar("D", bound=BaseDocument)


class MongoGenericRepository(Generic[T, D], AbstractGenericRepository[T], ABC):

    def __init__(
        self,
        model_cls: Type[D],
        mapper: Type[Mapper[T, D]],
        session: AsyncIOMotorClientSession | None,
    ):
        self._model_cls = model_cls
        self._mapper = mapper
        self._session = session

    async def get_by_id(self, id: UniqueEntityId) -> Optional[T]:
        doc = await self._model_cls.get(
            id.value, session=self._session, fetch_links=True
        )
        return await self._mapper.to_domain(doc) if doc else None

    async def get_one(self, **filters) -> T | None:
        doc = await self._model_cls.find_one(
            filters, session=self._session, fetch_links=True
        )
        return await self._mapper.to_domain(doc) if doc else None

    async def get(self, limit: int = 0, skip: int = 0, **filters) -> List[T]:
        query = (
            self._model_cls.find(filters, session=self._session, fetch_links=True)
            .limit(limit)
            .skip(skip)
        )
        docs = await query.to_list()
        return [await self._mapper.to_domain(doc) for doc in docs]

    async def create(self, entity: T) -> T:
        doc = await self._mapper.to_model(entity)
        created_doc = await doc.insert(
            link_rule=WriteRules.WRITE, session=self._session
        )

        return await self._mapper.to_domain(created_doc)

    async def update(self, entity: T) -> T:
        doc = await self._mapper.to_model(entity)
        updatedDoc = await doc.save(link_rule=WriteRules.WRITE, session=self._session)

        return await self._mapper.to_domain(updatedDoc)

    async def delete(self, id: UniqueEntityId) -> None:
        document = await self._model_cls.get(id)
        if document:
            await document.delete(
                link_rule=DeleteRules.DELETE_LINKS, session=self._session
            )
