from fazaconta_backend.shared.application.exceptions import ApplicationException


class GroupNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__("Group not found")


class PaidByNotFoundInGroupException(ApplicationException):
    def __init__(self):
        super().__init__("Paid by user not found in group")


class ParticipantNotFoundInGroupException(ApplicationException):
    def __init__(self):
        super().__init__(f"Participant not found in group")
