from fazaconta_backend.modules.user.useCases.getUser.GetUserResponse import (
    GetUserResponse,
)
from fazaconta_backend.shared.domain.UseCase import IUseCase
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class GetUsersUseCase(IUseCase[None, list[GetUserResponse]]):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self) -> list[GetUserResponse]:

        async with self.uow as uow:
            users = await uow.users.list()

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
