from uuid import UUID
from pydantic import BaseModel

from fazaconta_backend.modules.user.domain.UserDetail import UserDetail


class ParticipantDTO(BaseModel):
    user: UserDetail
    amount_to_pay: float
    id: UUID | None = None
