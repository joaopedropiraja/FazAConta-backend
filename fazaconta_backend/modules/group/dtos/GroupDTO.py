from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from .MemberDTO import MemberDTO
from .PendingPaymentDTO import PendingPaymentDTO

from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.shared.domain.files.FileData import FileData


class GroupDTO(BaseModel):
    title: str
    created_by: UserDetail
    total_expense: float
    created_at: datetime
    members: list[MemberDTO]
    pending_payments: list[PendingPaymentDTO]
    image: FileData | None = None
    id: UUID | None = None
