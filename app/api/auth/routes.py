"""API routes for user authentication and management."""

from fastapi import APIRouter
from app.api.auth.schemas import UserCreate, UserResponse
from app.api.auth.controller import (
    create_user_logic,
    list_users_logic,
    revoke_user_logic,
)
# TODO: verificação de token PARA que SÓ admins criem outros usuários
# from app.auth import verify_token

router = APIRouter()


@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Cria um novo usuário e retorna o token de acesso."""
    return create_user_logic(user.username, user.token)


@router.get("/list")
async def list_users():
    """Lista todos os usuários cadastrados."""
    return list_users_logic()


@router.delete("/revoke/{username}")
async def revoke_user(username: str):
    """Revoga o acesso de um usuário."""
    return revoke_user_logic(username)
