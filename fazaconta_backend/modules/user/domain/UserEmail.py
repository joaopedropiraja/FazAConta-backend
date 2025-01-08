from pydantic import EmailStr
from fazaconta_backend.shared.domain.ValueObject import ValueObject


class UserEmail(ValueObject):
    value: EmailStr
