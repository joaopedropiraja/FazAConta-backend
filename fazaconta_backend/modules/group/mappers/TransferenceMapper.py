from typing import Any
from fazaconta_backend.modules.group.domain.Transference import (
    Transference,
    TransferenceType,
)
from fazaconta_backend.modules.group.dtos.TransferenceDTO import TransferenceDTO
from fazaconta_backend.modules.group.infra.models.TransferenceDocument import (
    TransferenceDocument,
)
from fazaconta_backend.modules.group.mappers.GroupMapper import GroupMapper
from fazaconta_backend.modules.group.mappers.ParticipantMapper import ParticipantMapper
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper


class TransferenceMapper(Mapper[Transference, TransferenceDocument]):

    @staticmethod
    async def to_domain(model: TransferenceDocument) -> Transference:
        id = UniqueEntityId(model.id)
        group = await GroupMapper.to_domain(model.group)
        paid_by = await UserMapper.to_domain(model.paid_by)
        transference_type = TransferenceType(model.transference_type)
        participants = [
            await ParticipantMapper.to_domain(p) for p in model.participants
        ]

        return Transference(
            id=id,
            group=group,
            title=model.title,
            amount=model.amount,
            paid_by=paid_by,
            transference_type=transference_type,
            created_at=model.created_at,
            participants=participants,
        )

    @staticmethod
    async def to_model(entity: Transference) -> TransferenceDocument:
        group = await GroupMapper.to_model(entity.group)
        paid_by = await UserMapper.to_model(entity.paid_by)
        participants = [
            await ParticipantMapper.to_model(p) for p in entity.participants
        ]

        return TransferenceDocument(
            id=entity.id.value,
            group=group,
            title=entity.title,
            amount=entity.amount,
            paid_by=paid_by,
            transference_type=entity.transference_type,
            created_at=entity.created_at,
            participants=participants,
        )

    @staticmethod
    def to_dto(entity: Transference) -> Any:
        group = GroupMapper.to_group_detail(entity.group)
        paid_by = UserMapper.to_user_detail(entity.paid_by)
        participants = [ParticipantMapper.to_dto(p) for p in entity.participants]

        return TransferenceDTO(
            id=entity.id.value,
            group=group,
            title=entity.title,
            amount=entity.amount,
            paid_by=paid_by,
            transference_type=entity.transference_type,
            created_at=entity.created_at,
            participants=participants,
        )
