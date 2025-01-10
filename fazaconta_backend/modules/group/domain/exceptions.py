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


# Transference
class ParticipantsTotalAmountNotEqualToTransferenceAmountException(DomainException):
    def __init__(self):
        super().__init__(
            "The total amount to be paid by the participants needs to be equal to transfer amount"
        )


class ParticipantsListHasMoreThanOneUserException(DomainException):
    def __init__(self):
        super().__init__("Invalid participants list")
