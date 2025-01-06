import re

from fazaconta_backend.modules.user.domain.exceptions import InvalidPhoneNumber
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.ValueObject import ValueObject


class UserPhoneNumber(ValueObject):
    def __init__(self, number: str | None):
        Guard.against_undefined(argument=number, argument_name="phone_number")

        if not UserPhoneNumber.is_valid(number):  # type: ignore
            raise InvalidPhoneNumber()

        self.number = UserPhoneNumber.format(number)  # type: ignore

    @property
    def value(self) -> str:
        return self.number

    @staticmethod
    def is_valid(number: str) -> bool:
        """
        Validates a Brazilian phone number format, allowing for variations such as:
          +55 11 91234-5678
          (11) 91234-5678
          11 91234-5678
          11912345678
        etc.
        """
        re_pattern = r"^(\+55\s?)?(\(?\d{2}\)?\s?)?9?\d{4}-?\d{4}$"
        return re.match(re_pattern, number.strip()) is not None

    @staticmethod
    def format(number: str) -> str:
        return number.strip()
