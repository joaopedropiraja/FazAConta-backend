from datetime import datetime

from beanie import Link
from fazaconta_backend.modules.transference.domain.Participant import Participant
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument


class TransferenceDocument(BaseDocument):
    # group: Link[GroupDocument]
    title: str
    # amount: float
    paid_by: Link[UserDocument]
    # transference_type: str
    # date: datetime
    # participants: list[Participant]

    class Settings:
        name = "transferences"
