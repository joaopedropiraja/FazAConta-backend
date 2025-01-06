import re

from fazaconta_backend.modules.user.domain.exceptions import InvalidEmail
from fazaconta_backend.shared.domain.ValueObject import ValueObject


class UserEmail(ValueObject):
    def __init__(self, email: str):
        if not UserEmail.is_valid(email):
            raise InvalidEmail()

        self.email = UserEmail.format(email)

    @property
    def value(self) -> str:
        return self.email

    @staticmethod
    def is_valid(email: str) -> bool:
        re_pattern = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        return re.match(re_pattern, email) is not None

    @staticmethod
    def format(email: str) -> str:
        return email.strip().lower()
