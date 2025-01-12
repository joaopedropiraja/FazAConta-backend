from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class PendingPayment(Entity):
    def __init__(
        self,
        from_user: User,
        to_user: User,
        amount: float,
        id: UniqueEntityId | None = None,
    ):
        Guard.against_undefined_bulk(
            [
                {"argument": from_user, "argument_name": "from_user"},
                {"argument": to_user, "argument_name": "to_user"},
                {"argument": amount, "argument_name": "amount"},
            ]
        )
        Guard.greater_than(0, amount)

        super().__init__(id)

        self._from_user = from_user
        self._to_user = to_user
        self._amount = amount

    @property
    def from_user(self) -> User:
        return self._from_user

    @property
    def to_user(self) -> User:
        return self._to_user

    @property
    def amount(self) -> float:
        return self._amount
