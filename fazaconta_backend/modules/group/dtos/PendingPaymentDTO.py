from uuid import UUID
from pydantic import BaseModel, Field

from fazaconta_backend.modules.user.domain.UserDetail import UserDetail


class PendingPaymentDTO(BaseModel):
    id: UUID
    from_user: UserDetail
    to_user: UserDetail
    amount_to_be_paid: float = Field(ge=0)
