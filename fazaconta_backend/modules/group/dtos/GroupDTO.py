from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, field_serializer

from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO
from .MemberDTO import MemberDTO
from .PendingPaymentDTO import PendingPaymentDTO
from fazaconta_backend.shared.domain.files.FileData import FileData


class GroupDTO(BaseModel):
    id: UUID
    title: str
    created_by: UserDTO
    total_expense: float
    created_at: datetime
    members: list[MemberDTO]
    pending_payments: list[PendingPaymentDTO]
    image: FileData | None = None

    @field_serializer("id")
    def serialize_dt(self, id: UUID, _info):
        return str(id)
