"""Schemas para gestão de usuários."""

from pydantic import BaseModel, Field
from typing import Optional, Annotated
from uuid import UUID


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Nome do usuário (único)",
    )

    token: Optional[
        Annotated[
            UUID,
            Field(
                description="Token personalizado opcional no formato UUID válido (ex: 12345678-1234-5678-9012-123456789012)"
            ),
        ]
    ] = None


class UserResponse(BaseModel):
    username: str
    token: str
    status: str
