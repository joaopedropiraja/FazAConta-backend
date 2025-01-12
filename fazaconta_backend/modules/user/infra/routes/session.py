from typing import Annotated
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from fazaconta_backend.modules.user.domain.jwt import JWTData
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
from fazaconta_backend.modules.user.useCases.logout.LogoutExceptions import (
    UserNotFoundException,
)
from fazaconta_backend.modules.user.useCases.logout.LogoutUseCase import LogoutUseCase
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)
from fazaconta_backend.shared.infra.http.dependencies import (
    AuthService,
    JWTBearer,
    UnitOfWork,
)


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


@sessions_router.post(
    f"{route}/logout",
    status_code=status.HTTP_200_OK,
    tags=["sessions"],
)
async def logout(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    auth_service: Annotated[IAuthService, Depends(AuthService())],
    jwt_data: Annotated[JWTData, Depends(JWTBearer())],
) -> JSONResponse:
    try:
        use_case = LogoutUseCase(uow, auth_service)
        await use_case.execute(jwt_data.user.id)

        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "User is logged out"}
        )
    except UserNotFoundException as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Not found",
                "errors": str(exc),
            },
        )
