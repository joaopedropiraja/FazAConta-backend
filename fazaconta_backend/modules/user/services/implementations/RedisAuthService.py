import jwt
from typing import Any
from redis.asyncio import Redis
from datetime import datetime, timedelta, timezone
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.modules.user.services.IAuthService import IAuthService
from fazaconta_backend.shared.infra.config.settings import Settings


class RedisAuthService(IAuthService):
    redis_client: Redis

    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client
        self.jwt_hash_name = "activeJwtClients"

        refresh_token_expire_time_in_seconds = (
            Settings().REFRESH_TOKEN_EXPIRE_MINUTES * 60
        )
        self.token_expire_time = refresh_token_expire_time_in_seconds

    def sign_jwt_tokens(self, user: User) -> tuple[str, str]:
        access_token_data = UserMapper.to_user_detail(user).model_dump()
        access_token_expire = datetime.now(timezone.utc) + timedelta(
            minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token_data.update({"exp": access_token_expire})
        access_token = jwt.encode(
            access_token_data, Settings().ACCESS_TOKEN_SECRET, Settings().ALGORITHM
        )

        refresh_token_data: dict[str, Any] = {"user_id": str(user.id.value)}
        refresh_token_expire = datetime.now(timezone.utc) + timedelta(
            minutes=Settings().REFRESH_TOKEN_EXPIRE_MINUTES
        )
        refresh_token_data.update({"exp": refresh_token_expire})
        refresh_token = jwt.encode(
            refresh_token_data, Settings().REFRESH_TOKEN_SECRET, Settings().ALGORITHM
        )

        return access_token, refresh_token

    async def save_authenticated_user(self, user: User, refresh_token: str) -> None:
        key = self._construct_key(user, refresh_token)
        await self.redis_client.set(key, refresh_token)

        await self.redis_client.expire(key, self.token_expire_time)

    async def de_authenticate_user(self, user: User) -> None:
        keys = await self.redis_client.keys(
            f"*{self.jwt_hash_name}.{str(user.id.value)}*"
        )
        if keys:
            await self.redis_client.delete(*keys)

    async def get_tokens(self, user: User) -> list[str]:
        keys = await self.redis_client.keys(
            f"*{self.jwt_hash_name}.{str(user.id.value)}*"
        )
        return [await self.redis_client.get(key) for key in keys]

    def _construct_key(self, user: User, refresh_token) -> str:
        return f"refresh-{refresh_token}.{self.jwt_hash_name}.{str(user.id.value)}"
