from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class Participant(Entity):
    def __init__(self, user: User, amount: float, id: UniqueEntityId | None = None):
        Guard.against_undefined_bulk(
            [
                {"argument": user, "argument_name": "user"},
                {"argument": amount, "argument_name": "amount"},
            ]
        )
        Guard.greater_than(0, amount)

        super().__init__(id)

        self._user = user
        self._amount = amount

    @property
    def user(self) -> User:
        return self._user

    @property
    def amount(self) -> float:
        return self._amount
