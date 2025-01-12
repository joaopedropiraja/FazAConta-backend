from typing import Any
from fazaconta_backend.modules.group.domain.Participant import Participant
from fazaconta_backend.modules.group.dtos.ParticipantDTO import ParticipantDTO
from fazaconta_backend.modules.group.infra.models.ParticipantDocument import (
    ParticipantDocument,
)
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper


class ParticipantMapper(Mapper[Participant, ParticipantDocument]):

    @staticmethod
    async def to_domain(model: ParticipantDocument) -> Participant:
        id = UniqueEntityId(model.id)
        user = await UserMapper.to_domain(model.user)

        return Participant(id=id, user=user, amount_to_pay=model.amount_to_pay)

    @staticmethod
    async def to_model(entity: Participant) -> ParticipantDocument:
        user = await UserMapper.to_model(entity.user)

        return ParticipantDocument(
            id=entity.id.value, user=user, amount_to_pay=entity.amount_to_pay
        )

    @staticmethod
    def to_dto(entity: Participant) -> Any:
        user = UserMapper.to_dto(entity.user)
        return ParticipantDTO(
            id=entity.id.value, user=user, amount_to_pay=entity.amount_to_pay
        )
