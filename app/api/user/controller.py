"""Controller de Gestão de Usuários."""

from fastapi import HTTPException

from app.services.auth_service import AuthService
from utils.logging import get_logger

logger = get_logger("users_controller")


def create_user_logic(username: str, token: str = None):
    try:
        return AuthService.create_user(username, token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Erro crítico: {e}")
        raise HTTPException(status_code=500, detail="Erro interno") from e


def list_users_logic():
    return AuthService.list_users()


def revoke_user_logic(username: str):
    try:
        return AuthService.revoke_user(username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
