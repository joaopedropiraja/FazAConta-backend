from typing import Any
from fazaconta_backend.modules.group.domain.Member import Member
from fazaconta_backend.modules.group.dtos.MemberDTO import MemberDTO
from fazaconta_backend.modules.group.infra.models.MemberDocument import MemberDocument
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.modules.user.mappers.UserMapper import UserMapper
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.Mapper import Mapper


class MemberMapper(Mapper[Member, MemberDocument]):
    @staticmethod
    async def to_domain(model: MemberDocument) -> Member:
        id = UniqueEntityId(model.id)
        user = await UserMapper.to_domain(model.user)
        return Member(id=id, user=user, balance=model.balance)

    @staticmethod
    async def to_model(entity: Member) -> MemberDocument:
        user = await UserMapper.to_model(entity.user)

        return MemberDocument(id=entity.id.value, user=user, balance=entity.balance)

    @staticmethod
    def to_dto(entity: Member) -> Any:
        user = UserMapper.to_user_detail(entity.user)

        return MemberDTO(id=entity.id.value, user=user, balance=entity.balance)
