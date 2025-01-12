import asyncio
from fazaconta_backend.modules.group.domain.Participant import Participant
from fazaconta_backend.modules.group.domain.Transaction import (
    Transaction,
    TransactionType,
)
from fazaconta_backend.modules.group.dtos.TransactionDTO import TransactionDTO
from fazaconta_backend.modules.group.mappers.TransactionMapper import (
    TransactionMapper,
)
from .CreateTransactionDTO import (
    CreateTransactionDTO,
)
from .CreateTransactionExceptions import (
    GroupNotFoundException,
    PaidByNotFoundInGroupException,
    ParticipantNotFoundInGroupException,
)
from fazaconta_backend.shared.application.UseCase import IUseCase
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)


class CreateTransactionUseCase(IUseCase[CreateTransactionDTO, TransactionDTO]):
    uow: AbstractUnitOfWork

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, dto: CreateTransactionDTO) -> TransactionDTO:

        async with self.uow as uow:
            found_group = await uow.groups.get_by_id(UniqueEntityId(dto.group_id))
            if not found_group:
                raise GroupNotFoundException()

            users_in_group_dict = {m.user.id.value: m.user for m in found_group.members}

            paid_by = users_in_group_dict.get(dto.paid_by_user_id)
            if paid_by is None:
                raise PaidByNotFoundInGroupException()

            participants = []
            for p in dto.participants:
                user = users_in_group_dict.get(p.user_id)
                if user is None:
                    raise ParticipantNotFoundInGroupException()

                participant = Participant(user=user, amount=p.amount)
                participants.append(participant)

            transaction_type = TransactionType(dto.transaction_type)

            created_transaction = await uow.transactions.create(
                Transaction(
                    group=found_group,
                    title=dto.title,
                    amount=dto.amount,
                    paid_by=paid_by,
                    transaction_type=transaction_type,
                    participants=participants,
                )
            )

            await asyncio.gather(
                *[
                    uow.pending_payments.delete(p.id)
                    for p in found_group.pending_payments
                ]
            )
            found_group.manage_new_transaction(
                transaction_type=created_transaction.transaction_type,
                paid_by=created_transaction.paid_by,
                participants=created_transaction.participants,
                amount=created_transaction.amount,
            )
            await uow.groups.update(found_group)

            created_transaction.group = found_group

            return TransactionMapper.to_dto(created_transaction)
