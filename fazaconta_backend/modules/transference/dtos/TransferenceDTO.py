from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from fazaconta_backend.modules.transference.domain.Participant import Participant
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail


class TransferenceDTO(BaseModel):
    id: UUID
    group_id: UUID
    title: str
    amount: float
    paid_by: UserDetail
    transference_type: str
    date: datetime
    participants: list[Participant]
