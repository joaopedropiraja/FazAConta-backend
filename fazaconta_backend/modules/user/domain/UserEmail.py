import re

from fazaconta_backend.shared.domain.ValueObject import ValueObject
from fazaconta_backend.shared.exceptions.DomainException import DomainException


class UserEmail(ValueObject):
    def __init__(self, email: str):
        if UserEmail.is_valid_email(email):
            self.email = UserEmail.format(email)
        else:
            raise DomainException("E-mail inválido.")

    @property
    def value(self) -> str:
        return self.email

    @staticmethod
    def is_valid_email(email: str) -> bool:
        re_pattern = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        return re.match(re_pattern, email) is not None

    @staticmethod
    def format(email: str) -> str:
        return email.strip().lower()
