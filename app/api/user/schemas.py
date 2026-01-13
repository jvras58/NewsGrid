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
        constr(
            min_length=36,
            max_length=36,
            pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
        )
    ] = Field(
        None,
        description="Token personalizado opcional no formato UUID (ex: 12345678-1234-5678-9012-123456789012)",
    )


class UserResponse(BaseModel):
    username: str
    token: str
    status: str
