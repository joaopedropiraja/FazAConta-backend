from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


# class Member(ValueObject):
#     user: UserDetail
#     balance: float = Field(default=0.0)


class Member(Entity):
    def __init__(
        self, user: "UserDetail", balance: float = 0.0, id: UniqueEntityId | None = None
    ):
        Guard.against_undefined(user, "user")
        Guard.greater_equal_than(0, balance)

        super().__init__(id)

        self._user = user
        self._balance = balance

    @property
    def user(self) -> UserDetail:
        return self._user

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float):
        Guard.greater_equal_than(0, value)
        self._balance = value
