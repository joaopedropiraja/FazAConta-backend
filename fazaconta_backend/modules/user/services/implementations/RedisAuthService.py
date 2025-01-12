import asyncio
import jwt
from uuid import UUID, uuid4
from redis.asyncio import Redis
from datetime import datetime, timedelta, timezone
from fazaconta_backend.modules.user.domain.User import User
from fazaconta_backend.modules.user.domain.jwt import JWTData
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.modules.user.services.IAuthService import IAuthService
from fazaconta_backend.shared.infra.config.settings import Settings


class RedisAuthService(IAuthService):
    redis_client: Redis

    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client
        self.jwt_hash_name = "activeJwtClients"
        self.token_expire_time = Settings().REFRESH_TOKEN_EXPIRE_SECONDS

    async def decode_access_token(self, token: str) -> JWTData | None:
        try:
            decoded = jwt.decode(
                token, Settings().ACCESS_TOKEN_SECRET, algorithms=[Settings().ALGORITHM]
            )
            return JWTData(**decoded)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def sign_jwt_tokens(self, user: User) -> tuple[str, str]:
        access_token_data = JWTData(user=UserMapper.to_dto(user)).model_dump()
        access_token_expire = datetime.now(timezone.utc) + timedelta(
            minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token_data.update({"exp": access_token_expire})
        access_token = jwt.encode(
            access_token_data, Settings().ACCESS_TOKEN_SECRET, Settings().ALGORITHM
        )

        refresh_token = uuid4().hex

        return access_token, refresh_token

    async def save_authenticated_user(self, user_id: str, refresh_token: str) -> None:
        key = self._construct_key(user_id, refresh_token)
        await self.redis_client.set(key, refresh_token)
        await self.redis_client.expire(key, self.token_expire_time)

    async def de_authenticate_user(self, user_id: str) -> None:
        keys = await self.redis_client.keys(f"*{self.jwt_hash_name}.{user_id}*")
        if keys:
            await self.redis_client.delete(*keys)

    async def get_tokens(self, user_id: str) -> list[str]:
        keys = await self.redis_client.keys(f"*{self.jwt_hash_name}.{user_id}*")
        return await asyncio.gather(*[self.redis_client.get(key) for key in keys])

    def _construct_key(self, user_id: str, refresh_token) -> str:
        return f"refresh-{refresh_token}.{self.jwt_hash_name}.{user_id}"
