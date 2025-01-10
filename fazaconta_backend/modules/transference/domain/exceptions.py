from fazaconta_backend.shared.domain.exceptions import DomainException


class ParticipantsTotalAmountNotEqualToTransferenceAmountException(DomainException):
    def __init__(self):
        super().__init__(
            "The total amount to be paid by the participants need to be equal to transference amount"
        )
