from beanie import Link

from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument


class PendingPaymentDocument(BaseDocument):
    from_user: Link[UserDocument]
    to_user: Link[UserDocument]
    amount_to_pay: float

    class Settings:
        name = "pending_payments"
