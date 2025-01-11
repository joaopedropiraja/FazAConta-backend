from uuid import UUID
from fastapi import UploadFile
from pydantic import BaseModel


class CreateGroupUseCaseDTO(BaseModel):
    title: str
    created_by_user_id: UUID
    image: UploadFile | None = None
