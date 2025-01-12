from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class Member(Entity):
    def __init__(
        self, user: User, balance: float = 0.0, id: UniqueEntityId | None = None
    ):
        Guard.against_undefined(user, "user")

        super().__init__(id)

        self._user = user
        self._balance = balance

    @property
    def user(self) -> User:
        return self._user

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float):
        self._balance = value
