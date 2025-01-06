from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.modules.user.useCases.getUser.GetUserDTO import GetUserDTO
from fazaconta_backend.modules.user.useCases.getUser.GetUserResponse import (
    GetUserResponse,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.application.exceptions import (
    ApplicationException,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class GetUserUseCase(IUseCase[GetUserDTO, GetUserResponse]):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, dto: GetUserDTO) -> GetUserResponse:

        async with self.uow as uow:
            foundUser = await uow.users.get_one(**dto.model_dump(exclude_none=True))
            if foundUser is None:
                raise ApplicationException("User not found.")

            return UserMapper.to_dto(foundUser)
