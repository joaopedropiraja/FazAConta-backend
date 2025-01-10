from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from fazaconta_backend.modules.group.domain.GroupDetail import GroupDetail
from fazaconta_backend.modules.group.dtos.ParticipantDTO import ParticipantDTO
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail


class TransferenceDTO(BaseModel):
    id: UUID
    group: GroupDetail
    title: str
    amount: float
    paid_by: UserDetail
    transference_type: str
    created_at: datetime
    participants: list[ParticipantDTO]
