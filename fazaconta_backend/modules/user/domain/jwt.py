from uuid import UUID
from pydantic import BaseModel


class JWTData(BaseModel):
    user_id: UUID
