import bcrypt

from fazaconta_backend.shared.domain.ValueObject import ValueObject
from fazaconta_backend.shared.exceptions.DomainException import DomainException


class UserPassword(ValueObject):
    password: str
    hashed: bool

    def __init__(self, password: str | None, hashed: bool = False):
        if not password:
            raise DomainException("A senha é obrigatória.")
        self.password = password
        self.hashed = hashed

    @property
    def value(self) -> str:
        return self.password

    def is_already_hashed(self) -> bool:
        return self.hashed

    async def compare_password(self, plain_text_password: str) -> bool:
        if self.is_already_hashed():
            return await self._bcrypt_compare(plain_text_password, self.password)
        return self.password == plain_text_password

    async def _bcrypt_compare(self, plain_text: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(plain_text.encode("utf-8"), hashed.encode("utf-8"))
        except ValueError:
            raise DomainException("Senha incorreta.")

    async def get_hashed_value(self) -> str:
        if self.is_already_hashed():
            return self.password

        return await self._hash_password(self.password)

    async def _hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")
