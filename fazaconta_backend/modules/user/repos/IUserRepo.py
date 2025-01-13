from abc import ABC
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.IGenericRepository import (
    IGenericRepository,
)


class IUserRepo(IGenericRepository[User], ABC): ...
