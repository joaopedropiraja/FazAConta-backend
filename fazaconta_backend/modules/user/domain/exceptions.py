from fazaconta_backend.shared.exceptions.DomainException import DomainException


class InvalidEmail(DomainException):
    def __init__(self):
        super().__init__("Invalid or badly formatted e-mail.")
