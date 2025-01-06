from uuid import UUID
from pydantic import BaseModel, Field


class GetUsersDTO(BaseModel):
    limit: int = Field(0, ge=0)
    skip: int = Field(0, ge=0)
    id: UUID | None = None
    user_name: str | None = None
    email: str | None = None
