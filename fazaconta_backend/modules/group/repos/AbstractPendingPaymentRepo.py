from abc import ABC
from fazaconta_backend.modules.group.domain.PendingPayment import PendingPayment
from fazaconta_backend.shared.domain.AbstractGenericRepository import (
    AbstractGenericRepository,
)


class AbstractPendingPaymentRepo(AbstractGenericRepository[PendingPayment], ABC): ...
