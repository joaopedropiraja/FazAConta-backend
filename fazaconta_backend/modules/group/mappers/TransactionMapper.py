from typing import Any
from fazaconta_backend.modules.group.domain.Transaction import (
    Transaction,
    TransactionType,
)
from fazaconta_backend.modules.group.dtos.TransactionDTO import TransactionDTO
from fazaconta_backend.modules.group.infra.models.TransactionDocument import (
    TransactionDocument,
)
from fazaconta_backend.modules.group.mappers.GroupMapper import GroupMapper
from fazaconta_backend.modules.group.mappers.ParticipantMapper import ParticipantMapper
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper


class TransactionMapper(Mapper[Transaction, TransactionDocument]):

    @staticmethod
    async def to_domain(model: TransactionDocument) -> Transaction:
        id = UniqueEntityId(model.id)
        group = await GroupMapper.to_domain(model.group)
        paid_by = await UserMapper.to_domain(model.paid_by)
        transaction_type = TransactionType(model.transaction_type)
        participants = [
            await ParticipantMapper.to_domain(p) for p in model.participants
        ]

        return Transaction(
            id=id,
            group=group,
            title=model.title,
            amount=model.amount,
            paid_by=paid_by,
            transaction_type=transaction_type,
            created_at=model.created_at,
            participants=participants,
        )

    @staticmethod
    async def to_model(entity: Transaction) -> TransactionDocument:
        group = await GroupMapper.to_model(entity.group)
        paid_by = await UserMapper.to_model(entity.paid_by)
        participants = [
            await ParticipantMapper.to_model(p) for p in entity.participants
        ]

        return TransactionDocument(
            id=entity.id.value,
            group=group,
            title=entity.title,
            amount=entity.amount,
            paid_by=paid_by,
            transaction_type=entity.transaction_type,
            created_at=entity.created_at,
            participants=participants,
        )

    @staticmethod
    def to_dto(entity: Transaction) -> Any:
        group = GroupMapper.to_dto(entity.group)
        paid_by = UserMapper.to_dto(entity.paid_by)
        participants = [ParticipantMapper.to_dto(p) for p in entity.participants]

        return TransactionDTO(
            id=entity.id.value,
            group=group,
            title=entity.title,
            amount=entity.amount,
            paid_by=paid_by,
            transaction_type=entity.transaction_type,
            created_at=entity.created_at,
            participants=participants,
        )
