from fazaconta_backend.modules.user.useCases.getUser.GetUserDTO import GetUserDTO
from fazaconta_backend.modules.user.useCases.getUser.GetUserResponse import (
    GetUserResponse,
)
from fazaconta_backend.shared.domain.UseCase import IUseCase
from fazaconta_backend.shared.exceptions.ApplicationException import (
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

            return GetUserResponse(
                id=str(foundUser.id),
                user_name=foundUser.user_name,
                email=foundUser.email.value,
                image_src=foundUser.image_src,
                pix=foundUser.pix,
            )
