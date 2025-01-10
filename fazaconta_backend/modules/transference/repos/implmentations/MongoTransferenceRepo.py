from fazaconta_backend.modules.transference.domain.Transference import Transference
from fazaconta_backend.modules.transference.infra.models.TransferenceDocument import (
    TransferenceDocument,
)
from fazaconta_backend.modules.transference.repos.AbstractTransferenceRepo import (
    AbstractTransferenceRepo,
)
from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.repos.AbstractUserRepo import AbstractUserRepo
from fazaconta_backend.shared.infra.database.mongodb.GenericMongoRepository import (
    GenericMongoRepository,
)


class MongoTransferenceRepo(
    GenericMongoRepository[Transference, TransferenceDocument], AbstractTransferenceRepo
):
    async def get_by_group_id(self, group_id: str) -> Transference | None:
        return await self.get_one(group_id=group_id)
