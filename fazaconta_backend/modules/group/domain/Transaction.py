from datetime import datetime
from fazaconta_backend.modules.group.domain.Group import Group
from fazaconta_backend.modules.group.domain.Participant import Participant
from fazaconta_backend.modules.group.domain.TransactionType import TransactionType
from fazaconta_backend.modules.group.domain.exceptions import (
    ParticipantsListHasMoreThanOneUserException,
    ParticipantsTotalAmountNotEqualToTransactionAmountException,
    PayerUserNotInParticipantsListException,
)
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class Transaction(Entity):
    def __init__(
        self,
        group: Group,
        title: str,
        amount: float,
        paid_by: User,
        transaction_type: TransactionType,
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
                {"argument": transaction_type, "argument_name": "transaction_type"},
                {"argument": participants, "argument_name": "participants"},
                {"argument": created_at, "argument_name": "created_at"},
            ]
        )
        Guard.against_empty_str(argument=title, argument_name="title")
        Guard.against_empty_list(argument=participants, argument_name="participants")
        Guard.is_one_of_enum(
            value=transaction_type, enum_class=TransactionType, argument_name="type"
        )
        Guard.greater_than(0, amount)

        super().__init__(id)

        self._participants = participants
        self._transaction_type = transaction_type
        self._check_transaction_type()

        self._paid_by = paid_by
        self._check_payer_user_in_participants()

        self._amount = amount
        self._check_participants_amount()

        self._group = group
        self._title = title
        self._created_at = created_at

    def _check_payer_user_in_participants(self):
        if self.transaction_type != TransactionType.EXPENSE:
            return

        participant_ids = [p.user.id for p in self.participants]
        if self.paid_by.id not in participant_ids:
            raise PayerUserNotInParticipantsListException()

    def _check_participants_amount(self):
        total_amount_to_be_paid = sum([p.amount for p in self.participants])
        if self.amount != total_amount_to_be_paid:
            raise ParticipantsTotalAmountNotEqualToTransactionAmountException()

    def _check_transaction_type(self):
        if self.transaction_type == TransactionType.EXPENSE:
            return

        # Em envios de dinheiro ou reembolsos, a lista de participantes deve possuir uma única pessoa
        if len(self.participants) != 1:
            raise ParticipantsListHasMoreThanOneUserException()

    @property
    def group(self) -> Group:
        return self._group

    @group.setter
    def group(self, group: Group) -> None:
        self._group = group

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
    def transaction_type(self) -> TransactionType:
        return self._transaction_type

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def participants(self) -> list[Participant]:
        return self._participants
