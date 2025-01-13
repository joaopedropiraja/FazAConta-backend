from fazaconta_backend.modules.group.domain.Group import Group
from fazaconta_backend.modules.group.infra.models.GroupDocument import GroupDocument
from fazaconta_backend.modules.group.repos.IGroupRepo import IGroupRepo
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.mongodb.MongoGenericRepository import (
    MongoGenericRepository,
)


class MongoGroupRepo(MongoGenericRepository[Group, GroupDocument], IGroupRepo):
    async def get_by_user_id(
        self, user_id: UniqueEntityId, limit: int, skip: int
    ) -> list[Group]:
        pipeline = [
            {
                "$lookup": {
                    "from": "members",
                    "localField": "members.$id",
                    "foreignField": "_id",
                    "as": "members",
                }
            },
            {"$match": {"members.user.$id": user_id.value}},
            {"$project": {"_id": 1}},
        ]

        result = await GroupDocument.aggregate(
            pipeline,
        ).to_list()
        group_ids = [g["_id"] for g in result]

        groups = (
            await self._model_cls.find(
                {"_id": {"$in": group_ids}}, fetch_links=True, session=self._session
            )
            .limit(limit)
            .skip(skip)
            .to_list()
        )
        return [await self._mapper.to_domain(g) for g in groups]
