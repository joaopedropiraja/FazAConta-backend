import re
from enum import Enum
from typing import Self

from pydantic import model_validator
from fazaconta_backend.modules.user.domain.exceptions import InvalidPixValue
from fazaconta_backend.shared.domain.ValueObject import ValueObject


class PixType(str, Enum):
    EMAIL = "email"
    CPF_CNPJ = "cpf_cnpj"
    PHONE_NUMBER = "phone_number"
    RANDOM = "random"


class Pix(ValueObject):
    type: str
    value: str

    @model_validator(mode="after")
    def validate_value_by_type(self) -> Self:
        if self.type == PixType.EMAIL:
            email_pattern = (
                r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@'
                r"((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|"
                r"(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
            )
            if not re.match(email_pattern, self.value):
                raise InvalidPixValue(f"Invalid email format for Pix: {self.value}")

        elif self.type == PixType.CPF_CNPJ:
            # Minimal example: check only digits, length 11 or 14, etc.
            digits_only = re.sub(r"\D", "", self.value)
            if not (len(digits_only) in [11, 14]):
                raise InvalidPixValue(f"Invalid CPF/CNPJ length for Pix: {self.value}")

        elif self.type == PixType.PHONE_NUMBER:
            # Example: simple check for a minimal phone pattern
            phone_pattern = r"^(\+55\s?)?(\(?\d{2}\)?\s?)?9?\d{4}-?\d{4}$"
            if not re.match(phone_pattern, self.value):
                raise InvalidPixValue(
                    f"Invalid phone number format for Pix: {self.value}"
                )

        return self

    # def __init__(self, type: PixType, value: str):

    #     Guard.against_undefined_bulk(
    #         [
    #             {"argument": type, "argumentName": "type"},
    #             {"argument": value, "argumentName": "value"},
    #         ]
    #     )
    #     Guard.is_one_of_enum(value=type, enum_class=PixType, argument_name="Pix")

    #     self._validate_value(value)

    #     self._type = type
    #     self._value = value

    # # ---------------------------
    # # Getters
    # # ---------------------------
    # @property
    # def type(self) -> PixType:
    #     return self._type

    # @property
    # def value(self) -> str:
    #     return self._value

    # def _validate_value(self, value: str) -> None:
    #     if self._type == PixType.EMAIL:
    #         email_pattern = (
    #             r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@'
    #             r"((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|"
    #             r"(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
    #         )
    #         if not re.match(email_pattern, value):
    #             raise InvalidPixValue(f"Invalid email format for Pix: {value}")

    #     elif self._type == PixType.CPF_CNPJ:
    #         # Minimal example: check only digits, length 11 or 14, etc.
    #         digits_only = re.sub(r"\D", "", value)
    #         if not (len(digits_only) in [11, 14]):
    #             raise InvalidPixValue(f"Invalid CPF/CNPJ length for Pix: {value}")

    #     elif self._type == PixType.PHONE_NUMBER:
    #         # Example: simple check for a minimal phone pattern
    #         phone_pattern = r"^(\+55\s?)?(\(?\d{2}\)?\s?)?9?\d{4}-?\d{4}$"
    #         if not re.match(phone_pattern, value):
    #             raise InvalidPixValue(f"Invalid phone number format for Pix: {value}")
