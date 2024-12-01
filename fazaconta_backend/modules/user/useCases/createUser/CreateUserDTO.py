from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    user_name: str
    email: str
    password: str
    image_src: str | None = None
    pix: str | None = None
