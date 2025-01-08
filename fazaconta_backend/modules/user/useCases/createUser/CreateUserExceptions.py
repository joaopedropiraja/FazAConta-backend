from fazaconta_backend.shared.application.exceptions import ApplicationException


class DuplicateEmailException(ApplicationException):
    def __init__(self):
        super().__init__("E-mail already taken")
