from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.repos.AbstractUserRepo import AbstractUserRepo
from fazaconta_backend.shared.infra.database.mongodb.GenericMongoRepository import (
    GenericMongoRepository,
)


class MongoUserRepo(GenericMongoRepository[User, UserDocument], AbstractUserRepo):

    async def find_by_email_or_user_name(
        self, email: str, user_name: str
    ) -> User | None:
        doc = await self._model_cls.find_one(
            {"$or": [{"email": email}, {"user_name": user_name}]}
        )
        return self._mapper.to_domain(doc) if doc else None
