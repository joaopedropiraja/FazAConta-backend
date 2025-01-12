from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from fastapi.responses import JSONResponse

from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO
from fazaconta_backend.modules.user.useCases.createUser.CreateUserDTO import (
    CreateUserDTO,
)
from fazaconta_backend.modules.user.useCases.createUser.CreateUserExceptions import (
    DuplicateEmailException,
)
from fazaconta_backend.modules.user.useCases.createUser.CreateUserUseCase import (
    CreateUserUseCase,
)
from fazaconta_backend.modules.user.useCases.getUserById.GetUserByIdExceptions import (
    UserNotFoundException,
)
from fazaconta_backend.modules.user.useCases.getUserById.GetUserByIdUseCase import (
    GetUserUseCase,
)
from fazaconta_backend.modules.user.useCases.getUsers.GetUsersDTO import GetUsersDTO
from fazaconta_backend.modules.user.useCases.getUsers.GetUsersUseCase import (
    GetUsersUseCase,
)
from fazaconta_backend.modules.user.useCases.login.LoginUseCase import LoginUseCase
from fazaconta_backend.shared.domain.files.AbstractFileHandler import (
    AbstractFileHandler,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)
from fazaconta_backend.shared.infra.http.dependencies import (
    FileHandler,
    UnitOfWork,
)

users_router = APIRouter()
route = "/users"


@users_router.post(
    route,
    status_code=status.HTTP_201_CREATED,
    response_model=UserDTO,
    tags=["users"],
)
async def create_user(
    name: Annotated[str, Form(...)],
    nickname: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    phone_number: Annotated[str, Form(...)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    file_handler: Annotated[AbstractFileHandler, Depends(FileHandler())],
    pix_type: Annotated[str | None, Form()] = None,
    pix_value: Annotated[str | None, Form()] = None,
    image: Annotated[UploadFile | None, File()] = None,
) -> UserDTO | JSONResponse:
    try:
        use_case = CreateUserUseCase(uow, file_handler)

        dto = CreateUserDTO(
            name=name,
            nickname=nickname,
            email=email,
            password=password,
            phone_number=phone_number,
            pix_type=pix_type,
            pix_value=pix_value,
            image=image,
        )

        return await use_case.execute(dto)
    except DuplicateEmailException as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": "Conflict",
                "errors": str(exc),
            },
        )


@users_router.get(
    route,
    status_code=status.HTTP_200_OK,
    response_model=list[UserDTO],
    tags=["users"],
)
async def get_users(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    dto: Annotated[GetUsersDTO, Query()],
) -> list[UserDTO]:
    use_case = GetUsersUseCase(uow)
    return await use_case.execute(dto)


@users_router.get(
    f"{route}/{{user_id}}",
    status_code=status.HTTP_200_OK,
    response_model=UserDTO,
    tags=["users"],
)
async def get_user_by_id(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    user_id: UUID,
) -> UserDTO | JSONResponse:
    try:
        use_case = GetUserUseCase(uow)
        return await use_case.execute(user_id)
    except UserNotFoundException as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Not found",
                "errors": str(exc),
            },
        )
