from typing import Annotated
from beanie import Indexed
from fazaconta_backend.shared.infra.database.mongodb.BaseDocument import BaseDocument


class UserDocument(BaseDocument):
    user_name: Annotated[str, Indexed(unique=True)]
    email: Annotated[str, Indexed(unique=True)]
    password: str
    image_src: str | None
    pix: str | None

    class Settings:
        name = "users"
