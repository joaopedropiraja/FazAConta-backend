from fazaconta_backend.shared.domain.exceptions import DomainException


class InvalidPhoneNumber(DomainException):
    def __init__(self):
        super().__init__("Invalid phone number")


class InvalidPixValue(DomainException):
    def __init__(self, message: str):
        super().__init__(message)
