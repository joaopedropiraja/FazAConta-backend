from fazaconta_backend.modules.transference.domain.Transference import (
    Transference,
    TransferenceType,
)
from fazaconta_backend.modules.transference.dtos.TransferenceDTO import TransferenceDTO
from fazaconta_backend.modules.transference.mappers.TransferenceMapper import (
    TransferenceMapper,
)
from fazaconta_backend.modules.transference.useCases.createTransference.CreateTransferenceDTO import (
    CreateTransferenceDTO,
)
from fazaconta_backend.modules.transference.useCases.createTransference.CreateTransferenceExceptions import (
    GroupNotFoundException,
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
            # found_group = await uow.group.get_by_id(dto.group_id)
            # if not found_group:
            #     raise GroupNotFoundException()

            group_id = UniqueEntityId(dto.group_id)
            transference_type = TransferenceType(dto.transference_type)

            created_transference = await uow.transferences.create(
                Transference(
                    group_id=group_id,
                    title=dto.title,
                    amount=dto.amount,
                    paid_by=dto.paid_by,
                    transference_type=transference_type,
                    participants=dto.participants,
                )
            )

            await uow.commit()

            return TransferenceMapper.to_dto(created_transference)
