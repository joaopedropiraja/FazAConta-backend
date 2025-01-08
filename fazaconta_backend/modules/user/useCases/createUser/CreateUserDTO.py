from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict

from fazaconta_backend.modules.user.domain.Device import Device
from fazaconta_backend.modules.user.domain.Pix import Pix


class CreateUserDTO(BaseModel):
    name: str
    nickname: str
    email: str
    password: str
    phone_number: str
    pix_type: str | None = None
    pix_value: str | None = None
    image: UploadFile | None = None

    model_config = ConfigDict(str_strip_whitespace=True)
