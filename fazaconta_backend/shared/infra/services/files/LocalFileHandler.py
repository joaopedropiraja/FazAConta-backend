import asyncio
import os
from typing import Coroutine
import uuid
from fastapi import UploadFile

from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.files.IFileHandler import (
    IFileHandler,
)
from fazaconta_backend.shared.domain.files.FileData import FileData
from fazaconta_backend.shared.domain.exceptions import DomainException
from fazaconta_backend.shared.infra.config.settings import Settings


class LocalFileHandler(IFileHandler):
    base_path: str

    async def upload(self, file: UploadFile) -> FileData:
        """
        Save a single file to the local filesystem.
        """
        Guard.against_undefined_bulk(
            [
                {"argument": file.filename, "argument_name": "filename"},
                {"argument": file.content_type, "argument_name": "content_type"},
                {"argument": file.size, "argument_name": "size"},
            ]
        )

        content = await file.read()

        key = f"{uuid.uuid4()}_{file.filename}"
        local_path = os.path.join(Settings().FILES_PATH, key)

        with open(local_path, "wb") as f:
            f.write(content)

        return FileData(
            key=key,
            src=f"http://{Settings().HOST}:{Settings().PORT}/files/{key}",
            size=len(content),
            filename=file.filename,  # type: ignore
            content_type=file.content_type,  # type: ignore
        )

    async def multi_upload(self, files: list[UploadFile]) -> list[FileData]:
        """
        Save multiple files to the local filesystem.
        """
        awaitable_file_data_list: list[Coroutine] = []
        for file in files:
            awaitable_file_data_list.append(self.upload(file))

        return await asyncio.gather(*awaitable_file_data_list)

    async def delete(self, file_key: str) -> None:
        """
        Delete a file from the local filesystem based on the file key.
        """
        local_path = os.path.join(Settings().FILES_PATH, file_key)

        if not os.path.exists(local_path):
            raise DomainException(f"File with key '{file_key}' does not exist.")

        try:
            os.remove(local_path)
        except OSError as e:
            raise DomainException(f"Failed to delete file: {e}")
