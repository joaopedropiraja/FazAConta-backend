from abc import ABC, abstractmethod
from fastapi import UploadFile

from fazaconta_backend.shared.domain.files.FileData import FileData


class IFileHandler(ABC):
    @abstractmethod
    async def upload(self, file: UploadFile) -> FileData: ...

    @abstractmethod
    async def multi_upload(self, files: list[UploadFile]) -> list[FileData]: ...

    @abstractmethod
    async def delete(self, file_key: str) -> None: ...
