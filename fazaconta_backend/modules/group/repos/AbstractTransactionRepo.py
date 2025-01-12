from abc import ABC, abstractmethod
from fazaconta_backend.modules.group.domain.Transaction import Transaction
from fazaconta_backend.shared.domain.AbstractGenericRepository import (
    AbstractGenericRepository,
)
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId


class AbstractTransactionRepo(AbstractGenericRepository[Transaction], ABC):
    @abstractmethod
    async def get_by_group_id(
        self, group_id: UniqueEntityId, limit: int, skip: int
    ) -> list[Transaction] | None: ...
