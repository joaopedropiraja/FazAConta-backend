from uuid import UUID
from pydantic import BaseModel, field_serializer
from fazaconta_backend.modules.user.domain.Pix import Pix
from fazaconta_backend.shared.domain.files.FileData import FileData


class UserDTO(BaseModel):
    id: UUID
    name: str
    nickname: str
    email: str
    phone_number: str
    profile_photo: FileData | None
    pix: Pix | None

    @field_serializer("id")
    def serialize_dt(self, id: UUID, _info):
        return str(id)
