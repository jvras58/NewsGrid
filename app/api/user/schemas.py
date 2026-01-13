"""Schemas para gestão de usuários."""

from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, description="Nome do usuário (único)")
    token: Optional[str] = Field(None, description="Token personalizado opcional")


class UserResponse(BaseModel):
    username: str
    token: str
    status: str
