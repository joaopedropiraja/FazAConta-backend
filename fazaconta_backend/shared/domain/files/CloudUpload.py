from abc import ABC, abstractmethod
from fastapi import UploadFile

from fazaconta_backend.shared.domain.files.FileData import FileData


class CloudUpload(ABC):
    def __init__(self, config: dict | None = None):
        self.config = config or {}

    # async def __call__(
    #     self, file: UploadFile | None = None, files: list[UploadFile] | None = None
    # ) -> FileData | list[FileData]:
    #     try:
    #         if file:
    #             return await self.upload(file=file)

    #         elif files:
    #             return await self.multi_upload(files=files)
    #         else:
    #             return FileData(
    #                 status=False,
    #                 error="No file or files provided",
    #                 message="No file or files provided",
    #             )
    #     except Exception as err:
    #         return FileData(
    #             status=False, error=str(err), message="File upload was unsuccessful"
    #         )

    @abstractmethod
    async def upload(self, file: UploadFile) -> FileData: ...

    @abstractmethod
    async def multi_upload(self, files: list[UploadFile]) -> list[FileData]: ...
