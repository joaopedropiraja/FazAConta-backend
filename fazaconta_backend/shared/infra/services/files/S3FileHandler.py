import asyncio
from urllib.parse import quote as urlencode
from functools import cache
import uuid
import boto3
from fastapi import UploadFile

from fazaconta_backend.shared.domain.files.AbstractFileHandler import (
    AbstractFileHandler,
)
from fazaconta_backend.shared.domain.files.FileData import FileData
from fazaconta_backend.shared.domain.exceptions import DomainException
from fazaconta_backend.shared.infra.config.settings import Settings


class S3FileHandler(AbstractFileHandler):
    @property
    @cache
    def client(self):
        key_id = Settings().AWS_ACCESS_KEY_ID
        access_key = Settings().AWS_SECRET_ACCESS_KEY
        region_name = Settings().AWS_REGION

        return boto3.client(
            "s3",
            region_name=region_name,
            aws_access_key_id=key_id,
            aws_secret_access_key=access_key,
            endpoint_url=(
                Settings().AWS_S3_URL if Settings().ENV == "development" else None
            ),
        )

    async def upload(self, file: UploadFile) -> FileData:
        if not file.filename or not file.content_type or not file.size:
            raise DomainException("Invalid file.")

        key = f"{uuid.uuid4()}{file.filename}"

        bucket = Settings().AWS_BUCKET_NAME
        await asyncio.to_thread(
            self.client.upload_fileobj,
            file.file,
            bucket,
            key,
        )

        url = f"{Settings().AWS_S3_URL}/{Settings().AWS_BUCKET_NAME}/{urlencode(key.encode("utf8"))}"

        return FileData(
            key=key,
            src=url,
            filename=file.filename,
            content_type=file.content_type,
            size=file.size,
        )

    async def multi_upload(self, files: list[UploadFile]):
        tasks = [asyncio.create_task(self.upload(file=file)) for file in files]
        return await asyncio.gather(*tasks)
