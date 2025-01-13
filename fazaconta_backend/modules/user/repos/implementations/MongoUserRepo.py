from fazaconta_backend.modules.user.infra.models.UserDocument import UserDocument
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.repos.IUserRepo import IUserRepo
from fazaconta_backend.shared.infra.database.mongodb.AbstractMongoGenericRepository import (
    AbstractMongoGenericRepository,
)


class MongoUserRepo(AbstractMongoGenericRepository[User, UserDocument], IUserRepo): ...
