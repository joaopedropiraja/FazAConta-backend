from typing import Annotated
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request
from jwt import decode
from fazaconta_backend.modules.user.domain.jwt import JWTData
from fazaconta_backend.modules.user.services.IAuthService import IAuthService
from fazaconta_backend.shared.domain.files.IFileHandler import (
    IFileHandler,
)


class UnitOfWork:
    def __call__(self, request: Request):
        return request.state.uow


class FileHandler:
    def __call__(self, request: Request) -> IFileHandler:
        return request.state.file_handler


class AuthService:
    def __call__(self, request: Request) -> IAuthService:
        return request.state.auth_service


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
        auth_service: Annotated[IAuthService, Depends(AuthService())],
    ) -> JWTData:
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme",
            )

        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme",
            )

        decoded = await auth_service.decode_access_token(credentials.credentials)
        if decoded is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
            )

        tokens = await auth_service.get_tokens(str(decoded.user.id))
        if len(tokens) == 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Auth token not found. User is probably not logged in. Please login again",
            )

        return decoded
