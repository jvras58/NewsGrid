"""Rotas de autenticação com JWT Bearer Token."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth.controller import get_current_user, login_logic
from app.api.auth.schemas import TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login compatível com OAuth2.

    - **username:** Seu nome de usuário
    - **password:** Seu token de acesso
    """
    return login_logic(form_data.username, form_data.password)


@router.get("/me")
async def get_me(username: str = Depends(get_current_user)):
    """Retorna informações do usuário autenticado via JWT."""
    return {"username": username, "status": "authenticated via JWT"}
