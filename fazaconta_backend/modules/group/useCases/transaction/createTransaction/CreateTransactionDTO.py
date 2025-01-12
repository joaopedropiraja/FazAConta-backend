from uuid import UUID
from pydantic import BaseModel


class ParticipantDTO(BaseModel):
    user_id: UUID
    amount_to_pay: float


class CreateTransactionRequest(BaseModel):
    group_id: UUID
    title: str
    amount: float
    transaction_type: str
    participants: list[ParticipantDTO]


class CreateTransactionDTO(BaseModel):
    group_id: UUID
    title: str
    amount: float
    paid_by_user_id: UUID
    transaction_type: str
    participants: list[ParticipantDTO]
