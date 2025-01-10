from abc import ABC
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.AbstractGenericRepository import (
    AbstractGenericRepository,
)


class AbstractUserRepo(AbstractGenericRepository[User], ABC): ...
