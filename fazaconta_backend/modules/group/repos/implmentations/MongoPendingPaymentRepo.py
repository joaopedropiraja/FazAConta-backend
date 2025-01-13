from fazaconta_backend.modules.group.domain.PendingPayment import PendingPayment
from fazaconta_backend.modules.group.infra.models.PendingPaymentDocument import (
    PendingPaymentDocument,
)
from fazaconta_backend.modules.group.repos.IPendingPaymentRepo import (
    IPendingPaymentRepo,
)
from fazaconta_backend.shared.infra.database.mongodb.MongoGenericRepository import (
    MongoGenericRepository,
)


class MongoPendingPaymentRepo(
    MongoGenericRepository[PendingPayment, PendingPaymentDocument],
    IPendingPaymentRepo,
): ...
