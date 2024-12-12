from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.useCases.createUser.CreateUserDTO import (
    CreateUserDTO,
)
from fazaconta_backend.modules.user.useCases.createUser.CreateUserResponse import (
    CreateUserResponse,
)
from fazaconta_backend.modules.user.useCases.createUser.CreateUserUseCase import (
    CreateUserUseCase,
)
from fazaconta_backend.modules.user.useCases.getUser.GetUserDTO import GetUserDTO
from fazaconta_backend.modules.user.useCases.getUser.GetUserResponse import (
    GetUserResponse,
)
from fazaconta_backend.modules.user.useCases.getUser.GetUserUseCase import (
    GetUserUseCase,
)
from fazaconta_backend.modules.user.useCases.getUsers.GetUsersUseCase import (
    GetUsersUseCase,
)
from fazaconta_backend.shared.domain.files.CloudUpload import CloudUpload
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)
from fazaconta_backend.shared.infra.di.dependencies import FileHandler, UnitOfWork

users_router = APIRouter()


@users_router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_name: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    file_handler: Annotated[CloudUpload, Depends(FileHandler())],
    pix: Annotated[str | None, Form()] = None,
    image: Annotated[UploadFile | None, File()] = None,
) -> CreateUserResponse:
    use_case = CreateUserUseCase(uow, file_handler)

    dto = CreateUserDTO(
        user_name=user_name, email=email, password=password, pix=pix, image=image
    )

    return await use_case.execute(dto)


@users_router.get("/users", status_code=status.HTTP_200_OK)
async def get_user(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
) -> list[GetUserResponse]:
    use_case = GetUsersUseCase(uow)
    return await use_case.execute()
