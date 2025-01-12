from fazaconta_backend.modules.user.domain.Pix import Pix
from fazaconta_backend.modules.user.domain.UserPhoneNumber import UserPhoneNumber
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.domain.UserEmail import UserEmail
from fazaconta_backend.modules.user.domain.UserPassword import UserPassword
from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.modules.user.useCases.createUser.CreateUserDTO import (
    CreateUserDTO,
)
from fazaconta_backend.modules.user.useCases.createUser.CreateUserExceptions import (
    DuplicateEmailException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.files.AbstractFileHandler import (
    AbstractFileHandler,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class CreateUserUseCase(IUseCase[CreateUserDTO, UserDTO]):
    uow: AbstractUnitOfWork
    file_handler: AbstractFileHandler

    def __init__(
        self, uow: AbstractUnitOfWork, file_handler: AbstractFileHandler
    ) -> None:
        self.uow = uow
        self.file_handler = file_handler

    async def execute(self, dto: CreateUserDTO) -> UserDTO:

        async with self.uow as uow:
            found_user = await uow.users.get_one(email=dto.email)
            if found_user is not None:
                raise DuplicateEmailException()

            email = UserEmail(value=dto.email)
            password = UserPassword(value=dto.password)
            phone_number = UserPhoneNumber(value=dto.phone_number)
            profile_photo = (
                await self.file_handler.upload(dto.image)
                if dto.image is not None
                else None
            )
            pix = (
                Pix(type=dto.pix_type, value=dto.pix_value)  # type: ignore
                if dto.pix_type is not None or dto.pix_value is not None
                else None
            )

            created_user = await uow.users.create(
                User(
                    email=email,
                    password=password,
                    name=dto.name,
                    nickname=dto.nickname,
                    phone_number=phone_number,
                    profile_photo=profile_photo,
                    pix=pix,
                    devices=None,
                )
            )

            return UserMapper.to_dto(created_user)
