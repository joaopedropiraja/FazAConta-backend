from uuid import UUID
from pydantic import BaseModel


class AddMemberDTO(BaseModel):
    user_id: UUID
    group_id: UUID
