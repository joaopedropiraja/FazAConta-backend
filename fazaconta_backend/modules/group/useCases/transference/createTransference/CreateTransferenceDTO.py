from uuid import UUID
from pydantic import BaseModel

from fazaconta_backend.modules.group.domain.Participant import Participant
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail


# class CreateTransferenceDTO(BaseModel):
#     group_id: UUID
#     title: str
#     amount: float
#     paid_by: UserDetail
#     transference_type: str
#     participants: list[Participant]
