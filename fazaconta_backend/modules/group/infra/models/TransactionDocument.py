from datetime import datetime

from beanie import Link
from pydantic import Field
from fazaconta_backend.modules.group.infra.models.GroupDocument import (
    GroupDocument,
)
from fazaconta_backend.modules.group.infra.models.ParticipantDocument import (
    ParticipantDocument,
)
from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument


class TransactionDocument(BaseDocument):
    group: Link[GroupDocument]
    title: str
    amount: float
    paid_by: Link[UserDocument]
    transaction_type: str
    created_at: datetime
    participants: list[Link[ParticipantDocument]]

    class Settings:
        name = "transactions"
