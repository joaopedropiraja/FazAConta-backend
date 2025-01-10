from beanie import Link

from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument


class MemberDocument(BaseDocument):
    user: Link[UserDocument]
    balance: float

    class Settings:
        name = "members"
