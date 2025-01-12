from uuid import UUID
from pydantic import BaseModel


class ParticipantDTO(BaseModel):
    user_id: UUID
    amount_to_pay: float


class CreateTransferenceRequest(BaseModel):
    group_id: UUID
    title: str
    amount: float
    transference_type: str
    participants: list[ParticipantDTO]


class CreateTransferenceDTO(BaseModel):
    group_id: UUID
    title: str
    amount: float
    paid_by_user_id: UUID
    transference_type: str
    participants: list[ParticipantDTO]
