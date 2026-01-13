"""Schemas para operações de autenticação de usuários."""

from typing import Optional
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., description="Nome do usuário (ex: admin)")

    token: Optional[str] = Field(None, description="Token personalizado (opcional)")


class UserResponse(BaseModel):
    username: str
    token: str
    status: str
