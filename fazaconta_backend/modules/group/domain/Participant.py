from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class Participant(Entity):
    def __init__(
        self, user: User, amount_to_pay: float, id: UniqueEntityId | None = None
    ):
        Guard.against_undefined_bulk(
            [
                {"argument": user, "argument_name": "user"},
                {"argument": amount_to_pay, "argument_name": "amount_to_pay"},
            ]
        )
        Guard.greater_than(0, amount_to_pay)

        super().__init__(id)

        self._user = user
        self._amount_to_pay = amount_to_pay

    @property
    def user(self) -> User:
        return self._user

    @property
    def amount_to_pay(self) -> float:
        return self._amount_to_pay
