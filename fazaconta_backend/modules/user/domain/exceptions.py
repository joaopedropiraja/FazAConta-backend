from fazaconta_backend.shared.domain.exceptions import DomainException


class InvalidPixValueException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)
