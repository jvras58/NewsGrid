"""Rotas de autenticação com JWT Bearer Token."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.controller import get_current_user, login_logic
from app.api.auth.schemas import TokenResponse
from app.core.database import get_db
from app.models.user import User
from utils.logging import get_logger
from utils.security import create_access_token

router = APIRouter()
logger = get_logger("auth_routes")

Session = Annotated[AsyncSession, Depends(get_db)]
get_current_user_dep = Annotated[User, Depends(get_current_user)]


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm],
    session: AsyncSession = Session,
):
    """
    Login compatível com OAuth2.

    - **username:** Seu nome de usuário
    - **password:** Sua senha
    """
    user = await login_logic(form_data.username, form_data.password, session)
    # TODO: não sei se faz muito sentido o create_acess_token estar aqui na rota...
    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"JWT gerado para: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_me(current_user: get_current_user_dep):
    """Retorna informações do usuário autenticado via JWT."""
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "status": "authenticated via JWT",
    }
