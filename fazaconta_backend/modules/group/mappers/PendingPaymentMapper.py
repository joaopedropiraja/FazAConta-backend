from typing import Any
from fazaconta_backend.modules.group.domain.PendingPayment import PendingPayment
from fazaconta_backend.modules.group.dtos.PendingPaymentDTO import PendingPaymentDTO
from fazaconta_backend.modules.group.infra.models.PendingPaymentDocument import (
    PendingPaymentDocument,
)
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper


class PendingPaymentMapper(Mapper[PendingPayment, PendingPaymentDocument]):

    @staticmethod
    async def to_domain(model: PendingPaymentDocument) -> PendingPayment:
        id = UniqueEntityId(model.id)
        from_user = await UserMapper.to_domain(model.from_user)
        to_user = await UserMapper.to_domain(model.to_user)

        return PendingPayment(
            id=id,
            from_user=from_user,
            to_user=to_user,
            amount_to_pay=model.amount_to_pay,
        )

    @staticmethod
    async def to_model(entity: PendingPayment) -> PendingPaymentDocument:
        from_user = await UserMapper.to_model(entity.from_user)
        to_user = await UserMapper.to_model(entity.to_user)

        return PendingPaymentDocument(
            id=entity.id.value,
            from_user=from_user,
            to_user=to_user,
            amount_to_pay=entity.amount_to_pay,
        )

    @staticmethod
    def to_dto(entity: PendingPayment) -> Any:
        from_user = UserMapper.to_user_detail(entity.from_user)
        to_user = UserMapper.to_user_detail(entity.to_user)

        return PendingPaymentDTO(
            id=entity.id.value,
            from_user=from_user,
            to_user=to_user,
            amount_to_pay=entity.amount_to_pay,
        )
