from typing import Annotated
from beanie import Indexed
from pydantic import BaseModel
from fazaconta_backend.modules.user.domain.Device import Device
from fazaconta_backend.modules.user.domain.Pix import Pix
from fazaconta_backend.shared.domain.files.FileData import FileData
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument


class UserDocument(BaseDocument):
    name: str
    nickname: str
    email: Annotated[str, Indexed(unique=True)]
    password: str
    phone_number: str
    profile_photo: FileData | None
    pix: Pix | None
    devices: list[Device] | None

    class Settings:
        name = "users"


# class UserDocument(BaseDocument):
#     user_name: Annotated[str, Indexed(unique=True)]
#     email: Annotated[str, Indexed(unique=True)]
#     password: str
#     image_src: str | None
#     pix: str | None


#     class Settings:
#         name = "users"
