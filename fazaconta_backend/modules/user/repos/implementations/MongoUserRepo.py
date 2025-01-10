from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.repos.AbstractUserRepo import AbstractUserRepo
from fazaconta_backend.shared.infra.database.mongodb.MongoGenericRepository import (
    MongoGenericRepository,
)


class MongoUserRepo(MongoGenericRepository[User, UserDocument], AbstractUserRepo): ...
