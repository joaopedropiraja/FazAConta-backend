from fazaconta_backend.shared.application.exceptions import ApplicationException


class GroupNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__("Group not found")
