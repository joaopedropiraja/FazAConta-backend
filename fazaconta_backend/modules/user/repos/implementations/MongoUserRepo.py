from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.repos.AbstractUserRepo import AbstractUserRepo
from fazaconta_backend.shared.infra.database.mongodb.GenericMongoRepository import (
    GenericMongoRepository,
)


class MongoUserRepo(GenericMongoRepository[User, UserDocument], AbstractUserRepo): ...
