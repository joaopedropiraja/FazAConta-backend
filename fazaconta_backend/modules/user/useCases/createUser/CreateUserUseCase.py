from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.domain.UserEmail import UserEmail
from fazaconta_backend.modules.user.domain.UserPassword import UserPassword
from fazaconta_backend.modules.user.useCases.createUser.CreateUserDTO import (
    CreateUserDTO,
)
from fazaconta_backend.modules.user.useCases.createUser.CreateUserResponse import (
    CreateUserResponse,
)
from fazaconta_backend.shared.domain.UseCase import IUseCase
from fazaconta_backend.shared.exceptions.ApplicationException import (
    ApplicationException,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class CreateUserUseCase(IUseCase[CreateUserDTO, CreateUserResponse]):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, request: CreateUserDTO) -> CreateUserResponse:

        async with self.uow as uow:
            found_user = await uow.users.find_by_email_or_user_name(
                request.email, request.user_name
            )
            if found_user is not None:
                raise ApplicationException("Email or username already registered.")

            email = UserEmail(request.email)
            password = UserPassword(request.password)

            new_user = User(
                user_name=request.user_name,
                email=email,
                password=password,
                image_src=request.image_src,
                pix=request.pix,
            )
            created_user = await uow.users.add(new_user)
            await uow.commit()

            return CreateUserResponse(
                id=created_user.id.value,
                user_name=created_user.user_name,
                email=created_user.email.value,
                password=created_user.password.value,
                image_src=created_user.image_src,
                pix=created_user.pix,
            )
