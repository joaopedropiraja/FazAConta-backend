from fazaconta_backend.modules.user.useCases.getUser.GetUserResponse import (
    GetUserResponse,
)
from fazaconta_backend.modules.user.useCases.getUsers.GetUsersDTO import GetUsersDTO
from fazaconta_backend.shared.domain.UseCase import IUseCase
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class GetUsersUseCase(IUseCase[GetUsersDTO, list[GetUserResponse]]):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, dto=GetUsersDTO) -> list[GetUserResponse]:

        async with self.uow as uow:
            limit = dto.limit
            skip = dto.skip

            filters = dto.model_dump(exclude_none=True)
            del filters["limit"]
            del filters["skip"]

            users = await uow.users.get(limit=limit, skip=skip, **filters)

            return [
                GetUserResponse(
                    id=str(user.id),
                    user_name=user.user_name,
                    email=user.email.value,
                    image_src=user.image_src,
                    pix=user.pix,
                )
                for user in users
            ]
