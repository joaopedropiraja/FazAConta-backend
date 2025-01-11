from uuid import UUID
from pydantic import BaseModel, Field


class GetGroupsByUserIdDTO(BaseModel):
    user_id: UUID

    limit: int = Field(0, ge=0)
    skip: int = Field(0, ge=0)
