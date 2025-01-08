from uuid import UUID

from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.modules.user.useCases.getUserById.GetUserByIdExceptions import (
    UserNotFoundException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.application.exceptions import (
    ApplicationException,
)
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class GetUserUseCase(IUseCase[UUID, UserDTO]):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UUID) -> UserDTO:

        async with self.uow as uow:
            foundUser = await uow.users.get_by_id(UniqueEntityId(user_id))
            if foundUser is None:
                raise UserNotFoundException()

            return UserMapper.to_dto(foundUser)
