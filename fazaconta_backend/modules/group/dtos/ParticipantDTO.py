from uuid import UUID
from pydantic import BaseModel, field_serializer

from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class ParticipantDTO(BaseModel):
    id: UUID
    user: UserDTO
    amount: float

    @field_serializer("id")
    def serialize_dt(self, id: UUID, _info):
        return str(id)
