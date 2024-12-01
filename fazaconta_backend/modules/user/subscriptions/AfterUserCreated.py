from fazaconta_backend.modules.user.events.UserCreated import UserCreated
from fazaconta_backend.shared.domain.events.DomainEvents import DomainEvents
from fazaconta_backend.shared.domain.events.IHandle import IHandle
from fazaconta_backend.shared.infra.config.logger import logger


class AfterUserCreated(IHandle):
    def __init__(self) -> None:
        self.setup_subscriptions()

    def setup_subscriptions(self) -> None:
        DomainEvents.register(self.on_user_created, UserCreated.__name__)

    def on_user_created(self, event: UserCreated) -> None:
        logger.info("Bateu aqui")
