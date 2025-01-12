from fazaconta_backend.modules.group.dtos.TransactionDTO import TransactionDTO
from fazaconta_backend.modules.group.mappers.TransactionMapper import (
    TransactionMapper,
)
from fazaconta_backend.modules.group.useCases.transaction.getTransactionsByGroupId.GetTransactionsByGroupIdDTO import (
    GetTransactionsByGroupIdDTO,
)
from fazaconta_backend.modules.group.useCases.transaction.getTransactionsByGroupId.GetTransactionsByGroupIdExceptions import (
    GroupNotFoundException,
    InvalidOperationException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class GetTransactionsByGroupIdUseCase(
    IUseCase[GetTransactionsByGroupIdDTO, list[TransactionDTO]]
):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, dto: GetTransactionsByGroupIdDTO) -> list[TransactionDTO]:

        async with self.uow as uow:
            found_group = await uow.groups.get_by_id(UniqueEntityId(dto.group_id))
            if not found_group:
                raise GroupNotFoundException()

            user_ids_in_group = [m.user.id.value for m in found_group.members]
            if dto.logged_user_id not in user_ids_in_group:
                raise InvalidOperationException()

            transactions = await uow.transactions.get_by_group_id(
                found_group.id, limit=dto.limit, skip=dto.skip
            )

            return [TransactionMapper.to_dto(t) for t in (transactions or [])]
