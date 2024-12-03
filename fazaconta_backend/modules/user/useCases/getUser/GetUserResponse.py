from uuid import UUID
from pydantic import BaseModel


class GetUserResponse(BaseModel):
    user_name: str
    email: str
    image_src: str | None = None
    pix: str | None = None
