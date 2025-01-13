from abc import ABC, abstractmethod
from fazaconta_backend.modules.group.domain.PendingPayment import PendingPayment
from fazaconta_backend.shared.domain.IGenericRepository import (
    IGenericRepository,
)


class IPendingPaymentRepo(IGenericRepository[PendingPayment], ABC):
    @abstractmethod
    async def delete_many(self, pending_payments: list[PendingPayment]) -> None: ...
