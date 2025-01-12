from uuid import UUID
from pydantic import BaseModel

from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class ParticipantDTO(BaseModel):
    id: UUID
    user: UserDTO
    amount_to_pay: float
