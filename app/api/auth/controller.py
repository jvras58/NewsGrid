"""Controller de Autenticação (Login/Logout)."""

from fastapi import Response, Request, HTTPException
from app.services.auth_service import AuthService
from utils.logging import get_logger
from utils.settings import settings

logger = get_logger("auth_controller")


def login_logic(token: str, response: Response):
    try:
        username = AuthService.authenticate_by_token(token)

        session_id = AuthService.create_session(username)

        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=86400,
            samesite="lax",
            secure=settings.secure_cookies,
            path="/",
        )

        logger.info(f"Login realizado: {username}")
        return {"message": "Login realizado", "user": username}

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


def logout_logic(request: Request, response: Response):
    session_id = request.cookies.get("session_id")

    AuthService.delete_session(session_id)

    response.delete_cookie("session_id")
    return {"message": "Logout realizado"}


def verify_session(request: Request):
    """Dependência para proteger rotas."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Não autenticado")

    username = AuthService.get_user_by_session(session_id)
    if not username:
        raise HTTPException(status_code=401, detail="Sessão expirada")

    return username
