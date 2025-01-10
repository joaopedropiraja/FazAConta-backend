from pydantic import Field

from fazaconta_backend.shared.domain.ValueObject import ValueObject

brazilian_phone_number_pattern = r"^(\+55\s?)?(\(?\d{2}\)?\s?)?9?\d{4}-?\d{4}$"


class UserPhoneNumber(ValueObject):
    value: str = Field(pattern=brazilian_phone_number_pattern)
