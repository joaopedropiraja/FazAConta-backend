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
from fazaconta_backend.shared.domain.files.CloudUpload import CloudUpload
from fazaconta_backend.shared.exceptions.ApplicationException import (
    ApplicationException,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class CreateUserUseCase(IUseCase[CreateUserDTO, CreateUserResponse]):
    uow: AbstractUnitOfWork
    file_handler: CloudUpload

    def __init__(self, uow: AbstractUnitOfWork, file_handler: CloudUpload) -> None:
        self.uow = uow
        self.file_handler = file_handler

    async def execute(self, request: CreateUserDTO) -> CreateUserResponse:

        async with self.uow as uow:
            found_user = await uow.users.find_by_email_or_user_name(
                request.email, request.user_name
            )
            if found_user is not None:
                raise ApplicationException("Email or username already registered.")

            uploaded_image = (
                await self.file_handler.upload(request.image)
                if request.image is not None
                else None
            )
            email = UserEmail(request.email)
            password = UserPassword(request.password)

            created_user = await uow.users.create(
                User(
                    user_name=request.user_name,
                    email=email,
                    password=password,
                    image_src=(
                        str(uploaded_image.src) if uploaded_image is not None else None
                    ),
                    pix=request.pix,
                )
            )
            await uow.commit()

            return CreateUserResponse(
                id=created_user.id.value,
                user_name=created_user.user_name,
                email=created_user.email.value,
                image_src=created_user.image_src,
                pix=created_user.pix,
            )
