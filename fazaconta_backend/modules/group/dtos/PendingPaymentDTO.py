from uuid import UUID
from pydantic import BaseModel, Field

from fazaconta_backend.modules.user.domain.UserDetail import UserDetail


class PendingPaymentDTO(BaseModel):
    from_user: UserDetail
    to_user: UserDetail
    amount_to_pay: float = Field(ge=0)
    id: UUID | None = None
