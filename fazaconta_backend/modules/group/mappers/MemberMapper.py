from fazaconta_backend.modules.group.domain.Member import Member
from fazaconta_backend.modules.group.infra.models.MemberDocument import MemberDocument
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.shared.infra.database.Mapper import Mapper


# class MemberMapper(Mapper[Member, MemberDocument]):
#     @staticmethod
#     async def to_domain(model: MemberDocument) -> Member:
#         user = UserDetail(
#             user_id=model.user.id,
#             email=model.user.email,
#             nickname=model.user.nickname,
#             pix=model.user.pix,
#         )

#         return Member(user=user, balance=model.balance)

#     # @staticmethod
#     # async def to_model(entity: Member) -> MemberDocument:
#     #     return MemberDocument()
