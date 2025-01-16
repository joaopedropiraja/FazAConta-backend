from uuid import UUID
from pydantic import BaseModel, Field, field_serializer

from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class PendingPaymentDTO(BaseModel):
    id: UUID
    from_user: UserDTO
    to_user: UserDTO
    amount: float = Field(ge=0)

    @field_serializer("id")
    def serialize_dt(self, id: UUID, _info):
        return str(id)
