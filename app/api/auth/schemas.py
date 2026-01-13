"""Schemas para autenticação e sessão."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    token: str = Field(..., description="O Token de acesso do usuário")


class CurrentUserResponse(BaseModel):
    username: str
    status: str
