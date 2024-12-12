from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from pydantic import BaseModel


class GetUserResponse(BaseModel):
    id: UniqueEntityId
    user_name: str
    email: str
    image_src: str | None = None
    pix: str | None = None
