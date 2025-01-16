from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl

from fazaconta_backend.shared.domain.files.FileData import FileData


class GetGroupsByUserIdDTO(BaseModel):
    user_id: UUID

    limit: int = Field(0, ge=0)
    skip: int = Field(0, ge=0)


class GetGroupByUserIdResponse(BaseModel):
    id: UUID
    title: str
    image_src: HttpUrl | str | None
