from uuid import UUID
from pydantic import BaseModel, Field
from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class MemberDTO(BaseModel):
    user: UserDTO
    balance: float = Field(default=0.0)
    id: UUID | None = None
