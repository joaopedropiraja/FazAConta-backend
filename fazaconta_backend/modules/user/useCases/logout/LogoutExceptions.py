from fazaconta_backend.shared.application.exceptions import ApplicationException


class UserNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__("User not found")
