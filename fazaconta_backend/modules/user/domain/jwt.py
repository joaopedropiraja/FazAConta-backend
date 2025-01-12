from pydantic import BaseModel
from fazaconta_backend.modules.user.dtos.UserDTO import UserDTO


class JWTData(BaseModel):
    user: UserDTO
