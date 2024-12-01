from fazaconta_backend.modules.user.subscriptions.AfterUserCreated import (
    AfterUserCreated,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


def init_user_handlers(uow: AbstractUnitOfWork):
    AfterUserCreated(uow)
