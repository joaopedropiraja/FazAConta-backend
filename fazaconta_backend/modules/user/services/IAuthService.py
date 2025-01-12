from abc import ABC, abstractmethod


from fazaconta_backend.modules.user.domain.User import User


class IAuthService(ABC):

    @abstractmethod
    def sign_jwt_tokens(self, user: User) -> tuple[str, str]: ...

    # @abstractmethod
    # def sign_jwt(self, data: JWTData) -> str: ...

    # @abstractmethod
    # async def decode_jwt(self, token: str) -> JWTData: ...

    # @abstractmethod
    # def create_refresh_token(self) -> str: ...

    # @abstractmethod
    # async def get_tokens(self, user_id: UUID) -> list[str]: ...

    @abstractmethod
    async def save_authenticated_user(self, user: User, refresh_token: str) -> None: ...

    @abstractmethod
    async def de_authenticate_user(self, user: User) -> None: ...

    @abstractmethod
    async def get_tokens(self, user: User) -> list[str]: ...

    @abstractmethod
    def _construct_key(self, user: User, refresh_token) -> str: ...

    # @abstractmethod
    # async def de_authenticate_user(self, user_id: UUID) -> None: ...

    # @abstractmethod
    # async def refresh_token_exists(self, refresh_token: str) -> bool: ...

    # @abstractmethod
    # async def get_user_id_from_refresh_token(self, refresh_token: str) -> str: ...
