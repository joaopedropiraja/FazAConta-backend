from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.dtos.ParticipantDTO import ParticipantDTO
from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class TransferenceDTO(BaseModel):
    group: GroupDTO
    title: str
    amount: float
    paid_by: UserDTO
    transference_type: str
    created_at: datetime
    participants: list[ParticipantDTO]
    id: UUID | None = None
