from uuid import UUID

from pydantic import field_serializer
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.shared.domain.ValueObject import ValueObject
from fazaconta_backend.shared.domain.files.FileData import FileData


class GroupDetail(ValueObject):
    group_id: UUID
    title: str
    created_by: UserDetail
    image: FileData | None

    @field_serializer("group_id")
    def serialize_dt(self, group_id: UUID, _info):
        return str(group_id)
