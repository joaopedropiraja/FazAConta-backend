from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.mappers.GroupMapper import GroupMapper
from fazaconta_backend.modules.group.useCases.group.getGroupsByUserId.GetGroupsByUserIdDTO import (
    GetGroupByUserIdResponse,
    GetGroupsByUserIdDTO,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.IUnitOfWork import (
    IUnitOfWork,
)


class GetGroupsByUserIdUseCase(
    IUseCase[GetGroupsByUserIdDTO, list[GetGroupByUserIdResponse]]
):
    uow: IUnitOfWork

    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self, dto: GetGroupsByUserIdDTO
    ) -> list[GetGroupByUserIdResponse]:

        async with self.uow as uow:
            groups = await uow.groups.get_by_user_id(
                user_id=UniqueEntityId(dto.user_id), limit=dto.limit, skip=dto.skip
            )

            return [
                GetGroupByUserIdResponse(
                    id=g.id.value,
                    title=g.title,
                    image_src=g.image.src if g.image is not None else None,
                )
                for g in groups
            ]
