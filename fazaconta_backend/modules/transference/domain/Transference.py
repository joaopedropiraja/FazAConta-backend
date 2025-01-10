from datetime import datetime
from enum import Enum
from fazaconta_backend.modules.transference.domain.Participant import Participant
from fazaconta_backend.modules.transference.domain.exceptions import (
    ParticipantsTotalAmountNotEqualToTransferenceAmountException,
)
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class TransferenceType(str, Enum):
    SEND = "send"
    EXPENSE = "expense"
    REIMBURSEMENT = "reimbursement"


class Transference(Entity):
    def __init__(
        self,
        group_id: UniqueEntityId,
        title: str,
        amount: float,
        paid_by: UserDetail,
        transference_type: TransferenceType,
        participants: list[Participant],
        date: datetime = datetime.now(),
        id: UniqueEntityId | None = None,
    ):
        Guard.against_undefined_bulk(
            [
                {"argument": group_id, "argumentName": "group_id"},
                {"argument": title, "argumentName": "title"},
                {"argument": amount, "argumentName": "amount"},
                {"argument": paid_by, "argumentName": "paid_by"},
                {"argument": transference_type, "argumentName": "transference_type"},
                {"argument": participants, "argumentName": "participants"},
                {"argument": date, "argumentName": "date"},
            ]
        )
        Guard.against_empty_str(argument=title, argument_name="title")
        Guard.against_empty_list(argument=participants, argument_name="participants")
        Guard.is_one_of_enum(
            value=transference_type, enum_class=TransferenceType, argument_name="type"
        )
        Guard.greater_than(0, amount)

        self.__check_participants_amount()

        self._id = id
        self._group_id = group_id
        self._title = title
        self._amount = amount
        self._paid_by = paid_by
        self._transference_type = transference_type
        self._date = date
        self._participants = participants

    @property
    def group_id(self) -> UniqueEntityId:
        return self._group_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def paid_by(self) -> UserDetail:
        return self._paid_by

    @property
    def transference_type(self) -> TransferenceType:
        return self._transference_type

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def participants(self) -> list[Participant]:
        return self._participants

    def __check_participants_amount(self):
        total_amount_to_be_paid = sum([p.amount_to_pay for p in self.participants])
        if self.amount != total_amount_to_be_paid:
            raise ParticipantsTotalAmountNotEqualToTransferenceAmountException()
