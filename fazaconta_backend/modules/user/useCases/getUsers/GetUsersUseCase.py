from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.modules.user.useCases.getUsers.GetUsersDTO import GetUsersDTO
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class GetUsersUseCase(IUseCase[GetUsersDTO, list[UserDTO]]):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, dto: GetUsersDTO) -> list[UserDTO]:

        async with self.uow as uow:
            limit = dto.limit
            skip = dto.skip

            filters = dto.model_dump(exclude_none=True)
            del filters["limit"]
            del filters["skip"]

            users = await uow.users.get(limit=limit, skip=skip, **filters)

            return [UserMapper.to_dto(user) for user in users]
