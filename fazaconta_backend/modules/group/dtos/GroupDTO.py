from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO
from .MemberDTO import MemberDTO
from .PendingPaymentDTO import PendingPaymentDTO
from fazaconta_backend.shared.domain.files.FileData import FileData


class GroupDTO(BaseModel):
    title: str
    created_by: UserDTO
    total_expense: float
    created_at: datetime
    members: list[MemberDTO]
    pending_payments: list[PendingPaymentDTO]
    image: FileData | None = None
    id: UUID | None = None
