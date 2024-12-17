from uuid import UUID
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    id: UUID
    user_name: str
    email: str
    image_src: str | None = None
    pix: str | None = None
