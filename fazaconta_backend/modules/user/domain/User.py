from fazaconta_backend.modules.user.domain.UserEmail import UserEmail
from fazaconta_backend.modules.user.domain.UserPassword import UserPassword
from fazaconta_backend.modules.user.events.UserCreated import UserCreated
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.exceptions.DomainException import DomainException


class User(Entity):
    user_name: str
    email: UserEmail
    password: UserPassword
    image_src: str | None
    pix: str | None

    def __init__(
        self,
        email: UserEmail,
        user_name: str,
        password: UserPassword,
        image_src: str | None = None,
        pix: str | None = None,
        id: UniqueEntityId | None = None,
    ):
        super().__init__(id)

        if email is None or password is None or user_name is None:
            raise DomainException("E-mail e nome de usuário são obrigatórios.")

        self.email = email
        self.password = password
        self.user_name = user_name
        self.image_src = image_src
        self.pix = pix

        is_new_user = id is None
        if is_new_user:
            self.add_domain_event(UserCreated(self.id))
