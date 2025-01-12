from fazaconta_backend.shared.application.exceptions import ApplicationException


class UnauthorizedAccessException(ApplicationException):
    def __init__(self, message: str):
        super().__init__(message)


class ForbiddenAccessException(ApplicationException):
    def __init__(self, message: str):
        super().__init__(message)
