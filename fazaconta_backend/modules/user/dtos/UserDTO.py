from uuid import UUID
from pydantic import BaseModel

from fazaconta_backend.modules.user.domain.Pix import Pix
from fazaconta_backend.shared.domain.files.FileData import FileData


class UserDTO(BaseModel):
    name: str
    nickname: str
    email: str
    phone_number: str
    profile_photo: FileData | None
    pix: Pix | None
    id: UUID | None = None
