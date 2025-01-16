from uuid import UUID
from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.mappers.GroupMapper import GroupMapper
from fazaconta_backend.modules.group.mappers.TransactionMapper import TransactionMapper
from fazaconta_backend.modules.group.useCases.group.getGroupById.GetGroupByIdDTO import (
    GetGroupByIdDTO,
    GetGroupByIdFullResponse,
    GetGroupByIdLimitedResponse,
)
from fazaconta_backend.modules.group.useCases.group.getGroupById.GetGroupByIdExceptions import (
    GroupNotFoundException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.IUnitOfWork import (
    IUnitOfWork,
)


class GetGroupByIdUseCase(
    IUseCase[GetGroupByIdDTO, GroupDTO | GetGroupByIdLimitedResponse]
):
    uow: IUnitOfWork

    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self, dto: GetGroupByIdDTO
    ) -> GetGroupByIdFullResponse | GetGroupByIdLimitedResponse:

        async with self.uow as uow:
            found_group = await uow.groups.get_by_id(UniqueEntityId(dto.group_id))
            if found_group is None:
                raise GroupNotFoundException()

            user_ids_in_group = [m.user.id.value for m in found_group.members]
            if dto.user_id in user_ids_in_group:
                transactions = (
                    await uow.transactions.get_by_group_id(
                        found_group.id, limit=0, skip=0
                    )
                ) or []

                group_dto = GroupMapper.to_dto(found_group)
                return GetGroupByIdFullResponse(
                    **group_dto.model_dump(),
                    transactions=[TransactionMapper.to_dto(t) for t in transactions]
                )
            else:
                return GetGroupByIdLimitedResponse(
                    id=found_group.id.value,
                    title=found_group.title,
                    image_src=(
                        found_group.image.src if found_group.image is not None else None
                    ),
                )
