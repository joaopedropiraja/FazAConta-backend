from fazaconta_backend.shared.application.exceptions import ApplicationException


class NewUserToEnterGroupNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__("User not found")


class GroupToBeAddedNewMemberNotFound(ApplicationException):
    def __init__(self):
        super().__init__("Group not found")
