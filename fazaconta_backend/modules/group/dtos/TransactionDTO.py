from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, field_serializer

from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.dtos.ParticipantDTO import ParticipantDTO
from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class TransactionDTO(BaseModel):
    id: UUID
    group: GroupDTO
    title: str
    amount: float
    paid_by: UserDTO
    transaction_type: str
    created_at: datetime
    participants: list[ParticipantDTO]

    @field_serializer("id")
    def serialize_dt(self, id: UUID, _info):
        return str(id)
