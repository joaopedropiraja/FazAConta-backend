from uuid import UUID

from pydantic import field_serializer
from fazaconta_backend.modules.user.domain.Pix import Pix
from fazaconta_backend.shared.domain.ValueObject import ValueObject


class UserDetail(ValueObject):
    user_id: UUID
    email: str
    nickname: str
    pix: Pix | None = None

    @field_serializer("user_id")
    def serialize_dt(self, user_id: UUID, _info):
        return str(user_id)
