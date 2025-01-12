from typing import Annotated
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from fazaconta_backend.modules.user.services.IAuthService import IAuthService
from fazaconta_backend.modules.user.useCases.login.LoginDTO import (
    LoginDTO,
    LoginDTOResponse,
)
from fazaconta_backend.modules.user.useCases.login.LoginExceptions import (
    ForbiddenAccessException,
    UnauthorizedAccessException,
)
from fazaconta_backend.modules.user.useCases.login.LoginUseCase import LoginUseCase
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)
from fazaconta_backend.shared.infra.http.dependencies import AuthService, UnitOfWork


sessions_router = APIRouter()
route = "/sessions"


@sessions_router.post(
    f"{route}/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginDTOResponse,
    tags=["sessions"],
)
async def login(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    auth_service: Annotated[IAuthService, Depends(AuthService())],
    dto: Annotated[LoginDTO, Body()],
) -> LoginDTOResponse | JSONResponse:
    try:
        use_case = LoginUseCase(uow, auth_service)
        return await use_case.execute(dto)
    except UnauthorizedAccessException as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "Unauthorized",
                "errors": str(exc),
            },
        )
    except ForbiddenAccessException as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "message": "Forbidden",
                "errors": str(exc),
            },
        )
