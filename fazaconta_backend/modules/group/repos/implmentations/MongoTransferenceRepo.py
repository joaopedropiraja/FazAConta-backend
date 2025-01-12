from fazaconta_backend.modules.group.domain.Transference import Transference
from fazaconta_backend.modules.group.infra.models.TransferenceDocument import (
    TransferenceDocument,
)
from fazaconta_backend.modules.group.repos.AbstractTransferenceRepo import (
    AbstractTransferenceRepo,
)
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.mongodb.MongoGenericRepository import (
    MongoGenericRepository,
)


class MongoTransferenceRepo(
    MongoGenericRepository[Transference, TransferenceDocument], AbstractTransferenceRepo
):
    async def get_by_group_id(
        self, group_id: UniqueEntityId, limit: int, skip: int
    ) -> list[Transference] | None:
        groups = (
            await self._model_cls.find(
                self._model_cls.group.id == group_id.value,
                fetch_links=True,
                session=self._session,
            )
            .limit(limit)
            .skip(skip)
            .to_list()
        )

        return [await self._mapper.to_domain(g) for g in groups]
