from fazaconta_backend.modules.user.subscriptions.AfterUserCreated import (
    AfterUserCreated,
)
from fazaconta_backend.shared.infra.database.IUnitOfWork import (
    IUnitOfWork,
)


def init_user_handlers(uow: IUnitOfWork):
    AfterUserCreated(uow)
