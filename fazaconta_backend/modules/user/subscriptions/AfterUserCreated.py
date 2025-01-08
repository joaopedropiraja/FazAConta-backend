from fazaconta_backend.modules.user.events.UserCreated import UserCreated
from fazaconta_backend.shared.domain.events.DomainEvents import DomainEvents
from fazaconta_backend.shared.domain.events.IHandle import IHandle
from fazaconta_backend.shared.infra.config.logger import logger
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class AfterUserCreated(IHandle):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow
        self.setup_subscriptions()

    def setup_subscriptions(self) -> None:
        DomainEvents.register(self.on_user_created, UserCreated.__name__)

    def on_user_created(self, event: UserCreated) -> None:
        logger.info("Usuário criado com sucesso!")
