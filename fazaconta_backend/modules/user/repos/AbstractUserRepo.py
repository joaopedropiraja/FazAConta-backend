from abc import ABC, abstractmethod
from typing import Awaitable
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.shared.domain.AbstractGenericRepository import (
    AbstractGenericRepository,
)
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument


class AbstractUserRepo(AbstractGenericRepository[User], ABC):
    ...
    # @abstractmethod
    # async def find_by_email_or_user_name(
    #     self, email: str, user_name: str
    # ) -> User | None: ...
