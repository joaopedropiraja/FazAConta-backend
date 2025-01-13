from fazaconta_backend.modules.user.services.IAuthService import IAuthService
from fazaconta_backend.modules.user.useCases.login.LoginDTO import (
    LoginDTO,
    LoginDTOResponse,
)
from fazaconta_backend.modules.user.useCases.login.LoginExceptions import (
    UnauthorizedAccessException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.infra.database.IUnitOfWork import (
    IUnitOfWork,
)


class LoginUseCase(IUseCase[LoginDTO, LoginDTOResponse]):
    uow: IUnitOfWork
    auth_service: IAuthService

    def __init__(self, uow: IUnitOfWork, auth_service: IAuthService) -> None:
        self.uow = uow
        self.auth_service = auth_service

    async def execute(self, dto: LoginDTO) -> LoginDTOResponse:
        async with self.uow as uow:
            found_user = await uow.users.get_one(email=dto.email)
            if found_user is None:
                raise UnauthorizedAccessException("Wrong e-mail or password")

            is_match = await found_user.password.compare_password(dto.password)
            if not is_match:
                raise UnauthorizedAccessException("Wrong e-mail or password")

            access_token, refresh_token = self.auth_service.sign_jwt_tokens(found_user)
            user_id = str(found_user.id.value)
            await self.auth_service.save_authenticated_user(user_id, refresh_token)

            return LoginDTOResponse(
                access_token=access_token, refresh_token=refresh_token
            )
