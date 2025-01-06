import asyncio
import os
from typing import Coroutine
import uuid
from fastapi import UploadFile

from fazaconta_backend.shared.domain.files.CloudUpload import CloudUpload
from fazaconta_backend.shared.domain.files.FileData import FileData
from fazaconta_backend.shared.exceptions.DomainException import DomainException
from fazaconta_backend.shared.infra.config.settings import Settings


class LocalFileHandler(CloudUpload):
    base_path: str

    async def upload(self, file: UploadFile) -> FileData:
        """
        Save a single file to the local filesystem.
        """
        if not file.filename or not file.content_type or not file.size:
            raise DomainException("Invalid file.")

        content = await file.read()

        key = f"{uuid.uuid4()}{file.filename}"
        local_path = os.path.join(Settings().FILES_PATH, key)

        with open(local_path, "wb") as f:
            f.write(content)

        return FileData(
            key=key,
            src=f"http://{Settings().HOST}:{Settings().PORT}/files/{key}",
            size=len(content),
            filename=file.filename,
            content_type=file.content_type,
        )

    async def multi_upload(self, files: list[UploadFile]) -> list[FileData]:
        """
        Save multiple files to the local filesystem.
        """
        awaitable_file_data_list: list[Coroutine] = []
        for file in files:
            awaitable_file_data_list.append(self.upload(file))

        return await asyncio.gather(*awaitable_file_data_list)
