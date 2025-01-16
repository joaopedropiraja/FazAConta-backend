from uuid import UUID
from pydantic import BaseModel, Field, field_serializer
from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class MemberDTO(BaseModel):
    id: UUID
    user: UserDTO
    balance: float = Field(default=0.0)

    @field_serializer("id")
    def serialize_dt(self, id: UUID, _info):
        return str(id)
