from uuid import UUID
from pydantic import BaseModel
from fazaconta_backend.modules.group.dtos.ParticipantDTO import ParticipantDTO
from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class CreateTransferenceDTO(BaseModel):
    group_id: UUID
    title: str
    amount: float
    paid_by: UserDTO
    transference_type: str
    participants: list[ParticipantDTO]
