from datetime import datetime
from copy import deepcopy
from fazaconta_backend.modules.group.domain.Member import Member
from fazaconta_backend.modules.group.domain.Participant import Participant
from fazaconta_backend.modules.group.domain.PendingPayment import PendingPayment
from fazaconta_backend.modules.group.domain.TransactionType import TransactionType
from fazaconta_backend.modules.group.domain.exceptions import (
    GroupTotalBalanceDiffFromZeroException,
    MemberAlreadyInGroupException,
    MemberNotFoundInGroupException,
    PaymentsDoNotCoverMembersBalancesException,
    PendingPaymentNotFoundForReimbursementException,
)
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.domain.files.FileData import FileData


class Group(Entity):
    def __init__(
        self,
        title: str,
        created_by: User,
        total_expense: float = 0.0,
        created_at: datetime | None = None,
        members: list[Member] | None = None,
        pending_payments: list[PendingPayment] | None = None,
        image: FileData | None = None,
        id: UniqueEntityId | None = None,
    ):
        members = members or []
        pending_payments = pending_payments or []

        # Quando o grupo estiver sendo criado
        is_new_group = id is None
        if is_new_group:
            members.append(Member(user=created_by))
            created_at = datetime.now()

        Guard.against_undefined_bulk(
            [
                {"argument": title, "argument_name": "title"},
                {"argument": created_by, "argument_name": "created_by"},
                {"argument": created_at, "argument_name": "created_at"},
            ]
        )
        Guard.against_empty_str(argument=title, argument_name="title")

        super().__init__(id)

        self._members = members
        self._validate_members_total_balance()

        self._pending_payments = pending_payments
        self._validate_payments_amounts()

        self._title = title
        self._total_expense = total_expense
        self._image = image
        self._created_at = created_at
        self._created_by = created_by

    def add_member(self, member: Member):
        Guard.against_undefined(member, "member")
        if any(member.user.id.value == m.user.id.value for m in self.members):
            raise MemberAlreadyInGroupException()

        self._members.append(member)

    def manage_new_transaction(
        self,
        transaction_type: TransactionType,
        paid_by: User,
        participants: list[Participant],
        amount: float,
    ):
        Guard.against_undefined_bulk(
            [
                {"argument": transaction_type, "argument_name": "transaction_type"},
                {"argument": paid_by, "argument_name": "paid_by"},
                {"argument": participants, "argument_name": "participants"},
                {"argument": amount, "argument_name": "amount"},
            ]
        )
        Guard.against_empty_list(argument=participants, argument_name="participants")

        self._update_balances(paid_by, participants, amount)
        self._update_payments(transaction_type, paid_by, participants, amount)

        self._validate_members_total_balance()
        self._validate_payments_amounts()

    def _update_balances(
        self, paid_by: User, participants: list[Participant], amount: float
    ):
        members_dict = {m.user.id.value: m for m in self.members}
        for participant in participants:
            member = members_dict.get(participant.user.id.value)
            if member is None:
                raise MemberNotFoundInGroupException()

            member.balance -= participant.amount_to_pay

        payer = members_dict.get(paid_by.id.value)
        if payer is None:
            raise MemberNotFoundInGroupException()

        payer.balance += amount

    def _update_payments(
        self,
        transaction_type: TransactionType,
        paid_by: User,
        participants: list[Participant],
        amount: float,
    ):
        if transaction_type == TransactionType.REIMBURSEMENT:
            self._remove_pending_payment_related_to_reimbursement(paid_by, participants)
            return

        if transaction_type == TransactionType.EXPENSE:
            self._total_expense += amount

        self._pending_payments = []

        # Separate balances into two lists: positive and negative.
        pos: list[list] = []
        neg: list[list] = []
        for member in self.members:
            if member.balance > 0:
                pos.append([member.user, member.balance])
            elif member.balance < 0:
                neg.append([member.user, member.balance])

        # Sort lists:
        pos.sort(key=lambda x: x[1])  # smallest -> largest
        neg.sort(key=lambda x: x[1])  # most negative -> least negative

        # Greedy settle:
        # Use two pointers: i (for neg) from start, j (for pos) from end
        i = 0
        j = len(pos) - 1

        while i < len(neg) and j >= 0:
            debtor, debt_amount = neg[i]
            creditor, credit_amount = pos[j]

            # The amount to settle is the smaller (in absolute terms) of the two
            settle_amount = min(credit_amount, abs(debt_amount))

            pending_payment = PendingPayment(
                from_user=debtor, to_user=creditor, amount_to_pay=settle_amount
            )
            self._pending_payments.append(pending_payment)

            # Update balances after this payment

            # debt_amount += settle_amount (moves it toward 0)
            neg[i][1] += settle_amount
            # credit_amount -= settle_amount
            pos[j][1] -= settle_amount

            # If debtor is fully settled, move to the next debtor
            if neg[i][1] == 0:
                i += 1

            # If creditor is fully settled, move to the previous creditor
            if pos[j][1] == 0:
                j -= 1

    def _remove_pending_payment_related_to_reimbursement(
        self, paid_by: User, participants: list[Participant]
    ):
        for pending_payment in self._pending_payments:
            is_same_from_user = pending_payment.from_user.id.value == paid_by.id.value
            is_same_to_user = (
                pending_payment.to_user.id.value == participants[0].user.id.value
            )
            is_same_amount = (
                pending_payment.amount_to_pay == participants[0].amount_to_pay
            )

            if is_same_from_user and is_same_to_user and is_same_amount:
                self._pending_payments.remove(pending_payment)
                return

        raise PendingPaymentNotFoundForReimbursementException()

    def _validate_members_total_balance(self):
        total_balance = sum([m.balance for m in self.members])
        if total_balance != 0.0:
            raise GroupTotalBalanceDiffFromZeroException()

    def _validate_payments_amounts(self):
        members_dict = {m.user.id.value: m.balance for m in self.members}

        for payment in self.pending_payments:
            members_dict[payment.from_user.id.value] += payment.amount_to_pay
            members_dict[payment.to_user.id.value] -= payment.amount_to_pay

        if any(balance != 0.0 for balance in members_dict.values()):
            raise PaymentsDoNotCoverMembersBalancesException()

    @property
    def title(self) -> str:
        return self._title

    @property
    def image(self) -> FileData | None:
        return self._image

    @property
    def total_expense(self) -> float:
        return self._total_expense

    @property
    def created_by(self) -> User:
        return self._created_by

    @property
    def created_at(self) -> datetime:
        return self._created_at  # type: ignore

    @property
    def members(self) -> list[Member]:
        return self._members

    @property
    def pending_payments(self) -> list[PendingPayment]:
        return self._pending_payments
