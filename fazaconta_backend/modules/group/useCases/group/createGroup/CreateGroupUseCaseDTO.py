from pydantic import BaseModel

from fazaconta_backend.shared.domain.files.FileData import FileData


class CreateGroupUseCaseDTO(BaseModel):
    title: str
    image: FileData | None = None
