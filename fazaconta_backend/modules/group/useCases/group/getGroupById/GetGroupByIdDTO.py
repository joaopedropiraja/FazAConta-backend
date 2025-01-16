from uuid import UUID
from pydantic import BaseModel, HttpUrl

from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.dtos.TransactionDTO import TransactionDTO


class GetGroupByIdDTO(BaseModel):
    user_id: UUID
    group_id: UUID


class GetGroupByIdFullResponse(GroupDTO):
    transactions: list[TransactionDTO]


class GetGroupByIdLimitedResponse(BaseModel):
    id: UUID
    title: str
    image_src: HttpUrl | str | None
