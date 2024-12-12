from typing import Annotated
from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    user_name: str
    email: str
    password: str
    pix: str | None = None
    image: UploadFile | None = None
