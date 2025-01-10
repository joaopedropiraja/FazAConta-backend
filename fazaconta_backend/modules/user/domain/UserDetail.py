from uuid import UUID
from fazaconta_backend.modules.user.domain.Pix import Pix
from fazaconta_backend.shared.domain.ValueObject import ValueObject


class UserDetail(ValueObject):
    user_id: UUID
    email: str
    nickname: str
    pix: Pix | None = None
