from beanie import Link

from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument


class ParticipantDocument(BaseDocument):
    user: Link[UserDocument]
    amount: float

    class Settings:
        name = "participants"
