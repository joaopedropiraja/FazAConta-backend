from fazaconta_backend.shared.domain.exceptions import DomainException


# Group
class GroupTotalBalanceDiffFromZeroException(DomainException):
    def __init__(self):
        super().__init__(
            "The total balance (sum of each member's balances) needs to be 0"
        )


class PaymentsDoNotCoverMembersBalancesException(DomainException):
    def __init__(self):
        super().__init__(
            "The pending payments total amount need to turn every member balance equals to zero"
        )


class MemberAlreadyInGroupException(DomainException):
    def __init__(self):
        super().__init__("User is already in group")


class MemberNotFoundInGroupException(DomainException):
    def __init__(self):
        super().__init__("Member not found in group")


# Transference
class ParticipantsTotalAmountNotEqualToTransferenceAmountException(DomainException):
    def __init__(self):
        super().__init__(
            "The total amount to be paid by the participants needs to be equal to transfer amount"
        )


class ParticipantsListHasMoreThanOneUserException(DomainException):
    def __init__(self):
        super().__init__(
            "Participants list has more than one user in a send or reimbursement transfer"
        )


class PayerUserNotInParticipantsListException(DomainException):
    def __init__(self):
        super().__init__("The payer user needs to be in participants list")
