from typing import Any
from fastapi import Request
from fazaconta_backend.shared.domain.files.CloudUpload import CloudUpload


class UnitOfWork:
    def __call__(self, request: Request):
        return request.state.uow


class FileHandler:
    def __call__(self, request: Request) -> CloudUpload:
        return request.state.file_handler
