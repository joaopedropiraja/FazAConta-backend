from typing import Any
from fazaconta_backend.modules.group.domain.Group import Group
from fazaconta_backend.modules.group.domain.GroupDetail import GroupDetail
from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.infra.models.GroupDocument import GroupDocument
from fazaconta_backend.modules.group.mappers.MemberMapper import MemberMapper
from fazaconta_backend.modules.group.mappers.PendingPaymentMapper import (
    PendingPaymentMapper,
)
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper


class GroupMapper(Mapper[Group, GroupDocument]):

    @staticmethod
    async def to_domain(model: GroupDocument) -> Group:
        id = UniqueEntityId(model.id)
        created_by = await UserMapper.to_domain(model.created_by)
        members = [await MemberMapper.to_domain(m) for m in model.members]
        pending_payments = [
            await PendingPaymentMapper.to_domain(p) for p in model.pending_payments
        ]

        return Group(
            id=id,
            title=model.title,
            created_by=created_by,
            total_expense=model.total_expense,
            members=members,
            pending_payments=pending_payments,
            image=model.image,
            created_at=model.created_at,
        )

    @staticmethod
    async def to_model(entity: Group) -> GroupDocument:
        created_by = await UserMapper.to_model(entity.created_by)
        members = [await MemberMapper.to_model(m) for m in entity.members]
        pending_payments = [
            await PendingPaymentMapper.to_model(p) for p in entity.pending_payments
        ]

        return GroupDocument(
            id=entity.id.value,
            title=entity.title,
            created_by=created_by,
            total_expense=entity.total_expense,
            members=members,
            pending_payments=pending_payments,
            image=entity.image,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_dto(entity: Group) -> GroupDTO:
        created_by = UserMapper.to_user_detail(entity.created_by)
        members = [MemberMapper.to_dto(m) for m in entity.members]
        pending_payments = [
            PendingPaymentMapper.to_dto(p) for p in entity.pending_payments
        ]

        return GroupDTO(
            id=entity.id.value,
            title=entity.title,
            created_by=created_by,
            total_expense=entity.total_expense,
            created_at=entity.created_at,
            members=members,
            pending_payments=pending_payments,
            image=entity.image,
        )

    @staticmethod
    def to_group_detail(entity: Group) -> GroupDetail:
        created_by = UserMapper.to_user_detail(entity.created_by)
        return GroupDetail(
            group_id=entity.id.value,
            title=entity.title,
            created_by=created_by,
            image=entity.image,
        )
