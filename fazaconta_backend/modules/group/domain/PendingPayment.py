from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class PendingPayment(Entity):
    def __init__(
        self,
        from_user: User,
        to_user: User,
        amount_to_pay: float,
        id: UniqueEntityId | None = None,
    ):
        Guard.against_undefined_bulk(
            [
                {"argument": from_user, "argumentName": "from_user"},
                {"argument": to_user, "argumentName": "to_user"},
                {"argument": amount_to_pay, "argumentName": "amount_to_pay"},
            ]
        )
        Guard.greater_than(0, amount_to_pay)

        super().__init__(id)

        self._from_user = from_user
        self._to_user = to_user
        self._amount_to_pay = amount_to_pay

    @property
    def from_user(self) -> User:
        return self._from_user

    @property
    def to_user(self) -> User:
        return self._to_user

    @property
    def amount_to_pay(self) -> float:
        return self._amount_to_pay
