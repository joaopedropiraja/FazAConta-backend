from typing import Any
from uuid import UUID
from fazaconta_backend.modules.group.domain.Transference import (
    Transference,
    TransferenceType,
)
from fazaconta_backend.modules.group.dtos.TransferenceDTO import TransferenceDTO
from fazaconta_backend.modules.group.infra.models.TransferenceDocument import (
    TransferenceDocument,
)
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper


class TransferenceMapper(Mapper[Transference, TransferenceDocument]):

    @staticmethod
    async def to_domain(model: TransferenceDocument) -> Transference:
        ...
        # id = UniqueEntityId(model.id)
        # group_id = UniqueEntityId(UUID(model.group_id))
        # transference_type = TransferenceType(model.transference_type)

        # return Transference(
        #     id=id,
        #     group_id=group_id,
        #     title=model.title,
        #     amount=model.amount,
        #     paid_by=model.paid_by,
        #     transference_type=transference_type,
        #     date=model.date,
        #     participants=model.participants,
        # )

    @staticmethod
    async def to_model(entity: Transference) -> TransferenceDocument:
        ...
        # return TransferenceDocument(
        #     id=entity.id.value,
        #     # group_id=str(entity.group_id.value),
        #     title=entity.title,
        #     amount=entity.amount,
        #     paid_by=entity.paid_by,
        #     transference_type=entity.transference_type,
        #     date=entity.date,
        #     participants=entity.participants,
        # )

    @staticmethod
    def to_dto(entity: Transference) -> Any:
        ...
        # return TransferenceDTO(
        #     id=entity.id.value,
        #     group_id=entity.group_id.value,
        #     title=entity.title,
        #     amount=entity.amount,
        #     paid_by=entity.paid_by,
        #     transference_type=entity.transference_type,
        #     date=entity.date,
        #     participants=entity.participants,
        # )
