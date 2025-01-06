from pydantic import BaseModel


class UserDTO(BaseModel):
    id: str
    user_name: str
    email: str
    image_src: str | None = None
    pix: str | None = None
