from typing import Annotated
from fastapi import APIRouter, Depends, status
from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.modules.user.useCases.createUser.CreateUserDTO import (
    CreateUserDTO,
)
from fazaconta_backend.modules.user.useCases.createUser.CreateUserResponse import (
    CreateUserResponse,
)
from fazaconta_backend.modules.user.useCases.createUser.CreateUserUseCase import (
    CreateUserUseCase,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)
from fazaconta_backend.shared.infra.di.dependencies import UnitOfWork

users_router = APIRouter()


@users_router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_pokemon(
    body: CreateUserDTO, uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())]
) -> CreateUserResponse:
    # doc = UserDocument(**body.model_dump())
    # await doc.insert()

    # return doc
    use_case = CreateUserUseCase(uow)
    return await use_case.execute(body)
