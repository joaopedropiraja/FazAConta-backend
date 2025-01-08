import bcrypt
from pydantic import Field

from fazaconta_backend.shared.domain.ValueObject import ValueObject
from fazaconta_backend.shared.domain.exceptions import DomainException


class UserPassword(ValueObject):
    value: str
    hashed: bool = Field(default=False)

    def is_already_hashed(self) -> bool:
        return self.hashed

    async def compare_password(self, plain_text_password: str) -> bool:
        if self.is_already_hashed():
            return await self._bcrypt_compare(plain_text_password, self.value)
        return self.value == plain_text_password

    async def _bcrypt_compare(self, plain_text: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(plain_text.encode("utf-8"), hashed.encode("utf-8"))
        except ValueError:
            raise DomainException("Senha incorreta.")

    async def get_hashed_value(self) -> str:
        if self.is_already_hashed():
            return self.value

        return await self._hash_password(self.value)

    async def _hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")
