from fazaconta_backend.modules.group.domain.Member import Member
from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.mappers.GroupMapper import GroupMapper
from fazaconta_backend.modules.group.useCases.group.addMember.AddMemberDTO import (
    AddMemberDTO,
)
from fazaconta_backend.modules.group.useCases.group.addMember.AddMemberExceptions import (
    GroupToBeAddedNewMemberNotFound,
    NewUserToEnterGroupNotFoundException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class AddMemberUseCase(IUseCase[AddMemberDTO, GroupDTO]):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, dto: AddMemberDTO) -> GroupDTO:
        async with self.uow as uow:
            found_group = await uow.groups.get_by_id(UniqueEntityId(dto.group_id))
            if found_group is None:
                raise GroupToBeAddedNewMemberNotFound()

            found_user = await uow.users.get_by_id(UniqueEntityId(dto.user_id))
            if found_user is None:
                raise NewUserToEnterGroupNotFoundException()

            found_group.add_member(Member(user=found_user))
            updated_group = await uow.groups.update(found_group)

            return GroupMapper.to_dto(updated_group)
