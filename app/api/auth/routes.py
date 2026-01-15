"""Rotas de autenticação com JWT Bearer Token."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.controller import get_current_user, login
from app.api.auth.schemas import CurrentUserResponse, TokenResponse
from app.core.database import get_db
from app.models.user import User
from utils.logging import get_logger

router = APIRouter()
logger = get_logger("auth_routes")

Session = Annotated[AsyncSession, Depends(get_db)]
get_current_user_dep = Annotated[User, Depends(get_current_user)]


@router.post("/login", response_model=TokenResponse)
async def login_route(
    form_data: Annotated[OAuth2PasswordRequestForm],
    db=Session,
):
    """
    Login compatível com OAuth2.

    - **username:** Seu nome de usuário
    - **password:** Sua senha
    """
    access_token = await login(form_data.username, form_data.password, db)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=CurrentUserResponse)
async def get_me(current_user: get_current_user_dep):
    """Retorna informações do usuário autenticado via JWT."""
    return {
        "username": current_user.username,
        "status": "authenticated via JWT",
    }
