from uuid import UUID
from fazaconta_backend.modules.user.services.IAuthService import IAuthService
from fazaconta_backend.modules.user.useCases.logout.LogoutExceptions import (
    UserNotFoundException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class LogoutUseCase(IUseCase[UUID, None]):
    uow: AbstractUnitOfWork
    auth_service: IAuthService

    def __init__(self, uow: AbstractUnitOfWork, auth_service: IAuthService) -> None:
        self.uow = uow
        self.auth_service = auth_service

    async def execute(self, user_id: UUID) -> None:
        async with self.uow as uow:
            found_user = await uow.users.get_by_id(UniqueEntityId(user_id))
            if found_user is None:
                raise UserNotFoundException()

            await self.auth_service.de_authenticate_user(str(user_id))
