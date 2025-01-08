from uuid import UUID
from pydantic import BaseModel, Field


class GetUsersDTO(BaseModel):
    limit: int = Field(0, ge=0)
    skip: int = Field(0, ge=0)

    name: str | None = None
    nickname: str | None = None
    phone_number: str | None = None
    pix_value: str | None = None
