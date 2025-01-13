import asyncio
from fazaconta_backend.modules.group.domain.PendingPayment import PendingPayment
from fazaconta_backend.modules.group.infra.models.PendingPaymentDocument import (
    PendingPaymentDocument,
)
from fazaconta_backend.modules.group.repos.IPendingPaymentRepo import (
    IPendingPaymentRepo,
)
from fazaconta_backend.shared.infra.database.mongodb.AbstractMongoGenericRepository import (
    AbstractMongoGenericRepository,
)


class MongoPendingPaymentRepo(
    AbstractMongoGenericRepository[PendingPayment, PendingPaymentDocument],
    IPendingPaymentRepo,
):
    async def delete_many(self, pending_payments: list[PendingPayment]) -> None:
        tasks = [asyncio.create_task(self.delete(p.id)) for p in pending_payments]
        await asyncio.gather(*tasks)
