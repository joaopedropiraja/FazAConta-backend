from abc import ABC
from uuid import UUID
from fazaconta_backend.modules.group.domain.Group import Group
from fazaconta_backend.shared.domain.AbstractGenericRepository import (
    AbstractGenericRepository,
)
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class AbstractGroupRepo(AbstractGenericRepository[Group], ABC):

    async def get_by_user_id(
        self, user_id: UniqueEntityId, limit: int, skip: int
    ) -> list[Group]: ...
