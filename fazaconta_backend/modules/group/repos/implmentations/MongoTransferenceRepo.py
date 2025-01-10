from fazaconta_backend.modules.group.domain.Transference import Transference
from fazaconta_backend.modules.group.infra.models.TransferenceDocument import (
    TransferenceDocument,
)
from fazaconta_backend.modules.group.repos.AbstractTransferenceRepo import (
    AbstractTransferenceRepo,
)
from fazaconta_backend.shared.infra.database.mongodb.MongoGenericRepository import (
    MongoGenericRepository,
)


class MongoTransferenceRepo(
    MongoGenericRepository[Transference, TransferenceDocument], AbstractTransferenceRepo
):
    async def get_by_group_id(self, group_id: str) -> Transference | None:
        return await self.get_one(group_id=group_id)
