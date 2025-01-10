from datetime import datetime
from beanie import Link
from fazaconta_backend.modules.group.infra.models.MemberDocument import MemberDocument
from fazaconta_backend.modules.group.infra.models.PendingPaymentDocument import (
    PendingPaymentDocument,
)
from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.shared.domain.files.FileData import FileData
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument


class GroupDocument(BaseDocument):
    title: str
    created_by: Link[UserDocument]
    total_expense: float
    created_at: datetime
    members: list[Link[MemberDocument]]
    pending_payments: list[Link[PendingPaymentDocument]]
    image: FileData | None = None

    class Settings:
        name = "groups"
