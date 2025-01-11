from typing import Any
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.modules.user.domain.UserPhoneNumber import UserPhoneNumber
from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO
from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.domain.UserEmail import UserEmail
from fazaconta_backend.modules.user.domain.UserPassword import UserPassword
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper


class UserMapper(Mapper[User, UserDocument]):

    @staticmethod
    async def to_domain(model: UserDocument) -> User:
        id = UniqueEntityId(model.id)
        email = UserEmail(value=model.email)
        password = UserPassword(value=model.password, hashed=True)
        phone_number = UserPhoneNumber(value=model.phone_number)

        return User(
            id=id,
            email=email,
            password=password,
            phone_number=phone_number,
            name=model.name,
            nickname=model.nickname,
            pix=model.pix,
            devices=model.devices,
            profile_photo=model.profile_photo,
        )

    @staticmethod
    async def to_model(entity: User) -> UserDocument:
        if entity.password.is_already_hashed():
            password = entity.password.value
        else:
            password = await entity.password.get_hashed_value()

        return UserDocument(
            id=entity.id.value,
            email=entity.email.value,
            password=password,
            phone_number=entity.phone_number.value,
            name=entity.name,
            nickname=entity.nickname,
            pix=entity.pix,
            devices=entity.devices,
            profile_photo=entity.profile_photo,
        )

    @staticmethod
    def to_dto(entity: User) -> UserDTO:
        return UserDTO(
            id=entity.id.value,
            email=entity.email.value,
            phone_number=entity.phone_number.value,
            name=entity.name,
            nickname=entity.nickname,
            pix=entity.pix,
            profile_photo=entity.profile_photo,
        )

    @staticmethod
    def to_user_detail(entity: User) -> UserDetail:
        return UserDetail(
            user_id=entity.id.value,
            email=entity.email.value,
            nickname=entity.nickname,
            pix=entity.pix,
        )
