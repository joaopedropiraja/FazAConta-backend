from datetime import datetime
from typing import Any
from fazaconta_backend.modules.group.domain.Member import Member
from fazaconta_backend.modules.group.domain.PendingPayment import PendingPayment
from fazaconta_backend.modules.group.domain.exceptions import (
    GroupTotalBalanceDiffFromZeroException,
    MemberAlreadyInGroupException,
    PaymentsDoNotCoverMembersBalancesException,
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

    def manage_new_transference(self, transference: Any):
        Guard.against_undefined(transference, "transference")

        self._update_balances(transference)
        self._update_payments(transference)
        # Logic to distribute expenses among members based on transference
        pass

    def _update_balances(self, transference: Any):
        # Logic to update member balances
        ...

    def _update_payments(self, transference: Any):
        # Logic to resolve pending payments
        ...

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
