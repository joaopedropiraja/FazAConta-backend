from uuid import UUID
from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.mappers.GroupMapper import GroupMapper
from fazaconta_backend.modules.group.useCases.group.getGroupById.GetGroupByIdExceptions import (
    GroupNotFoundException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.IUnitOfWork import (
    IUnitOfWork,
)


class GetGroupByIdUseCase(IUseCase[UUID, GroupDTO]):
    uow: IUnitOfWork

    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, group_id: UUID) -> GroupDTO:

        async with self.uow as uow:
            found_group = await uow.groups.get_by_id(UniqueEntityId(group_id))
            if found_group is None:
                raise GroupNotFoundException()

            return GroupMapper.to_dto(found_group)
