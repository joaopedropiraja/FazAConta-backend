from pydantic import BaseModel


class LoginDTO(BaseModel):
    email: str
    password: str


class LoginDTOResponse(BaseModel):
    access_token: str
    refresh_token: str
