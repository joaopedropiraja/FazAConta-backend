from fazaconta_backend.modules.group.dtos.TransferenceDTO import TransferenceDTO
from fazaconta_backend.modules.group.mappers.TransferenceMapper import (
    TransferenceMapper,
)
from fazaconta_backend.modules.group.useCases.transference.getTransferencesByGroupId.GetTransferencesByGroupIdDTO import (
    GetTransferencesByGroupIdDTO,
)
from fazaconta_backend.modules.group.useCases.transference.getTransferencesByGroupId.GetTransferencesByGroupIdExceptions import (
    GroupNotFoundException,
    InvalidOperationException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class GetTransferencesByGroupIdUseCase(
    IUseCase[GetTransferencesByGroupIdDTO, list[TransferenceDTO]]
):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, dto: GetTransferencesByGroupIdDTO) -> list[TransferenceDTO]:

        async with self.uow as uow:
            found_group = await uow.groups.get_by_id(UniqueEntityId(dto.group_id))
            if not found_group:
                raise GroupNotFoundException()

            user_ids_in_group = [m.user.id.value for m in found_group.members]
            if dto.logged_user_id not in user_ids_in_group:
                raise InvalidOperationException()

            transferences = await uow.transferences.get_by_group_id(
                found_group.id, limit=dto.limit, skip=dto.skip
            )

            return [TransferenceMapper.to_dto(t) for t in (transferences or [])]
