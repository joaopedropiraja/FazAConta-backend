from pydantic import Field
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.shared.domain.ValueObject import ValueObject


class Participant(ValueObject):
    user: UserDetail
    amount_to_pay: float = Field(ge=0)
