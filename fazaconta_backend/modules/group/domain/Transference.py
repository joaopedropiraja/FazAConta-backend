from datetime import datetime
from enum import Enum
from fazaconta_backend.modules.group.domain.Group import Group
from fazaconta_backend.modules.group.domain.Participant import Participant
from fazaconta_backend.modules.group.domain.exceptions import (
    ParticipantsListHasMoreThanOneUserException,
    ParticipantsTotalAmountNotEqualToTransferenceAmountException,
)
from fazaconta_backend.modules.user.domain.User import User
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
        group: Group,
        title: str,
        amount: float,
        paid_by: User,
        transference_type: TransferenceType,
        participants: list[Participant],
        created_at: datetime = datetime.now(),
        id: UniqueEntityId | None = None,
    ):
        Guard.against_undefined_bulk(
            [
                {"argument": group, "argument_name": "group"},
                {"argument": title, "argument_name": "title"},
                {"argument": amount, "argument_name": "amount"},
                {"argument": paid_by, "argument_name": "paid_by"},
                {"argument": transference_type, "argument_name": "transference_type"},
                {"argument": participants, "argument_name": "participants"},
                {"argument": created_at, "argument_name": "created_at"},
            ]
        )
        Guard.against_empty_str(argument=title, argument_name="title")
        Guard.against_empty_list(argument=participants, argument_name="participants")
        Guard.is_one_of_enum(
            value=transference_type, enum_class=TransferenceType, argument_name="type"
        )
        Guard.greater_than(0, amount)

        super().__init__(id)

        self._participants = participants
        self._check_participants_amount()

        self._transference_type = transference_type
        self._check_transference_type()

        self._group = group
        self._title = title
        self._amount = amount
        self._paid_by = paid_by
        self._created_at = created_at

    def _check_participants_amount(self):
        total_amount_to_be_paid = sum([p.amount_to_pay for p in self.participants])
        if self.amount != total_amount_to_be_paid:
            raise ParticipantsTotalAmountNotEqualToTransferenceAmountException()

    def _check_transference_type(self):
        if self.transference_type == TransferenceType.EXPENSE:
            return

        # Em envios de dinheiro ou reembolsos, a lista de participantes deve possuir uma única pessoa
        if len(self.participants) != 1:
            raise ParticipantsListHasMoreThanOneUserException()

    @property
    def group(self) -> Group:
        return self._group

    @property
    def title(self) -> str:
        return self._title

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def paid_by(self) -> User:
        return self._paid_by

    @property
    def transference_type(self) -> TransferenceType:
        return self._transference_type

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def participants(self) -> list[Participant]:
        return self._participants
