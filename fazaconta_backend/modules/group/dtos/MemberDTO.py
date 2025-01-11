from uuid import UUID
from pydantic import BaseModel, Field

from fazaconta_backend.modules.user.domain.UserDetail import UserDetail


class MemberDTO(BaseModel):
    user: UserDetail
    balance: float = Field(default=0.0)
    id: UUID | None = None
