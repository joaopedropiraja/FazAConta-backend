from abc import ABC, abstractmethod
from fazaconta_backend.modules.group.domain.Transference import Transference
from fazaconta_backend.shared.domain.AbstractGenericRepository import (
    AbstractGenericRepository,
)
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class AbstractTransferenceRepo(AbstractGenericRepository[Transference], ABC):
    @abstractmethod
    async def get_by_group_id(
        self, group_id: UniqueEntityId, limit: int, skip: int
    ) -> list[Transference] | None: ...
