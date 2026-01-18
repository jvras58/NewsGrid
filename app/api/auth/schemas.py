from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class CurrentUserResponse(BaseModel):
    username: str
    status: str
