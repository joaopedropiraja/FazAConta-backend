from fazaconta_backend.modules.group.domain.Group import Group
from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.mappers.GroupMapper import GroupMapper
from fazaconta_backend.modules.group.useCases.group.createGroup.CreateGroupUseCaseDTO import (
    CreateGroupUseCaseDTO,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.domain.files.AbstractFileHandler import (
    AbstractFileHandler,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class CreateGroupUseCase(IUseCase[CreateGroupUseCaseDTO, GroupDTO]):
    uow: AbstractUnitOfWork
    file_handler: AbstractFileHandler

    def __init__(
        self, uow: AbstractUnitOfWork, file_handler: AbstractFileHandler
    ) -> None:
        self.uow = uow
        self.file_handler = file_handler

    async def execute(self, dto: CreateGroupUseCaseDTO) -> GroupDTO:

        async with self.uow as uow:
            created_by = await uow.users.get_by_id(
                UniqueEntityId(dto.created_by_user_id)
            )
            Guard.against_undefined(argument=created_by, argument_name="created_by")

            image = (
                await self.file_handler.upload(dto.image)
                if dto.image is not None
                else None
            )

            created_group = await uow.groups.create(
                Group(title=dto.title, created_by=created_by, image=image)  # type: ignore
            )

            return GroupMapper.to_dto(created_group)
