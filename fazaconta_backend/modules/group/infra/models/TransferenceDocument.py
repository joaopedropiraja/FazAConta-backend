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


class TransferenceDocument(BaseDocument):
    group: Link[GroupDocument]
    title: str
    amount: float
    paid_by: Link[UserDocument]
    transference_type: str
    date: datetime
    participants: list[Link[ParticipantDocument]]

    class Settings:
        name = "transferences"
