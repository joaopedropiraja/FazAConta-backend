from abc import ABC, abstractmethod
from fazaconta_backend.modules.group.domain.Group import Group
from fazaconta_backend.shared.domain.IGenericRepository import (
    IGenericRepository,
)
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class IGroupRepo(IGenericRepository[Group], ABC):

    @abstractmethod
    async def get_by_user_id(
        self, user_id: UniqueEntityId, limit: int, skip: int
    ) -> list[Group]: ...
