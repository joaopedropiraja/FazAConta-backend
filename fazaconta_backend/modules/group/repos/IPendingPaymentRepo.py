from abc import ABC
from fazaconta_backend.modules.group.domain.PendingPayment import PendingPayment
from fazaconta_backend.shared.domain.IGenericRepository import (
    IGenericRepository,
)


class IPendingPaymentRepo(IGenericRepository[PendingPayment], ABC): ...
