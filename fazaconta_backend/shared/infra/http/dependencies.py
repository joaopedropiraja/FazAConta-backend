from fastapi import Request
from fazaconta_backend.modules.user.services.IAuthService import IAuthService
from fazaconta_backend.shared.domain.files.AbstractFileHandler import (
    AbstractFileHandler,
)


class UnitOfWork:
    def __call__(self, request: Request):
        return request.state.uow


class FileHandler:
    def __call__(self, request: Request) -> AbstractFileHandler:
        return request.state.file_handler


class AuthService:
    def __call__(self, request: Request) -> IAuthService:
        return request.state.auth_service
