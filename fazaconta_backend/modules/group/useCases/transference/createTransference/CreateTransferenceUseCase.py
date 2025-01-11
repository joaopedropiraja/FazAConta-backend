from fazaconta_backend.modules.group.domain.Participant import Participant
from fazaconta_backend.modules.group.domain.Transference import (
    Transference,
    TransferenceType,
)
from fazaconta_backend.modules.group.dtos.TransferenceDTO import TransferenceDTO
from fazaconta_backend.modules.group.mappers.TransferenceMapper import (
    TransferenceMapper,
)
from fazaconta_backend.shared.domain.Guard import Guard
from .CreateTransferenceDTO import (
    CreateTransferenceDTO,
)
from .CreateTransferenceExceptions import (
    GroupNotFoundException,
    PaidByNotFoundInGroupException,
    ParticipantNotFoundInGroupException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class CreateTransferenceUseCase(IUseCase[CreateTransferenceDTO, TransferenceDTO]):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, dto: CreateTransferenceDTO) -> TransferenceDTO:

        async with self.uow as uow:
            found_group = await uow.groups.get_by_id(UniqueEntityId(dto.group_id))
            if not found_group:
                raise GroupNotFoundException()

            users_in_group_dict = {m.user.id.value: m.user for m in found_group.members}

            paid_by = users_in_group_dict.get(dto.paid_by.user_id)
            if paid_by is None:
                raise PaidByNotFoundInGroupException()

            participants = []
            for p in dto.participants:
                user = users_in_group_dict.get(p.user.user_id)
                if user is None:
                    raise ParticipantNotFoundInGroupException(p.user.nickname)

                participant = Participant(user=user, amount_to_pay=p.amount_to_pay)
                participants.append(participant)

            transference_type = TransferenceType(dto.transference_type)

            created_transference = await uow.transferences.create(
                Transference(
                    group=found_group,
                    title=dto.title,
                    amount=dto.amount,
                    paid_by=paid_by,
                    transference_type=transference_type,
                    participants=participants,
                )
            )

            found_group.manage_new_transference(created_transference)
            await uow.groups.update(found_group)

            await uow.commit()

            return TransferenceMapper.to_dto(created_transference)
