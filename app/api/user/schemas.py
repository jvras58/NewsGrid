"""Schemas para gestão de usuários."""

from pydantic import BaseModel, Field, constr
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Nome do usuário (único)",
    )
    token: Optional[
        constr(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    ] = Field(
        None,
        description="Token personalizado opcional (mín. 32 caracteres, apenas letras, números, '_' e '-')",
    )


class UserResponse(BaseModel):
    username: str
    token: str
    status: str
