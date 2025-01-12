from uuid import UUID
from pydantic import BaseModel

from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class ParticipantDTO(BaseModel):
    user: UserDTO
    amount_to_pay: float
    id: UUID | None = None
