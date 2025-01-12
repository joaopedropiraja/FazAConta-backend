from uuid import UUID
from pydantic import BaseModel, Field

from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class PendingPaymentDTO(BaseModel):
    from_user: UserDTO
    to_user: UserDTO
    amount_to_pay: float = Field(ge=0)
    id: UUID | None = None
