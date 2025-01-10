from uuid import UUID
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.shared.domain.ValueObject import ValueObject
from fazaconta_backend.shared.domain.files.FileData import FileData


class GroupDetail(ValueObject):
    group_id: UUID
    title: str
    description: str
    created_by: UserDetail
    image: FileData | None
