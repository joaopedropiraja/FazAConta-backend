from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.domain.UserEmail import UserEmail
from fazaconta_backend.modules.user.domain.UserPassword import UserPassword
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper


class UserMapper(Mapper[User, UserDocument]):

    async def to_domain(self, model: UserDocument) -> User:
        id = UniqueEntityId(model.id)
        email = UserEmail(model.email)
        password = UserPassword(model.password, hashed=True)

        return User(
            id=id,
            user_name=model.user_name,
            email=email,
            password=password,
            image_src=model.image_src,
            pix=model.pix,
        )

    async def to_model(self, entity: User) -> UserDocument:
        if entity.password.is_already_hashed():
            password = entity.password.value
        else:
            password = await entity.password.get_hashed_value()

        return UserDocument(
            id=entity.id.value,
            user_name=entity.user_name,
            email=entity.email.value,
            password=password,
            image_src=entity.image_src,
            pix=entity.pix,
        )
