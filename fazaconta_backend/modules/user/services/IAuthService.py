from abc import ABC, abstractmethod
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.domain.jwt import JWTData


class IAuthService(ABC):

    @abstractmethod
    def sign_jwt_tokens(self, user: User) -> tuple[str, str]: ...

    # @abstractmethod
    # def sign_jwt(self, data: JWTData) -> str: ...

    @abstractmethod
    async def decode_access_token(self, token: str) -> JWTData | None: ...

    # @abstractmethod
    # def create_refresh_token(self) -> str: ...

    # @abstractmethod
    # async def get_tokens(self, user_id: UUID) -> list[str]: ...

    @abstractmethod
    async def save_authenticated_user(
        self, user_id: str, refresh_token: str
    ) -> None: ...

    @abstractmethod
    async def de_authenticate_user(self, user_id: str) -> None: ...

    @abstractmethod
    async def get_tokens(self, user_id: str) -> list[str]: ...

    @abstractmethod
    def _construct_key(self, user_id: str, refresh_token) -> str: ...

    # @abstractmethod
    # async def de_authenticate_user(self, user_id: UUID) -> None: ...

    # @abstractmethod
    # async def refresh_token_exists(self, refresh_token: str) -> bool: ...

    # @abstractmethod
    # async def get_user_id_from_refresh_token(self, refresh_token: str) -> str: ...
