from uuid import UUID

from pydantic import BaseModel


class GetUserDTO(BaseModel):
    id: UUID | None = None
    user_name: str | None = None
    email: str | None = None
