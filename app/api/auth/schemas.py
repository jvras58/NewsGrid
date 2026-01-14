"""Schemas para autenticação JWT."""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Resposta do endpoint de login com JWT."""

    access_token: str
    token_type: str


class CurrentUserResponse(BaseModel):
    """Resposta do endpoint /me."""

    username: str
    status: str
