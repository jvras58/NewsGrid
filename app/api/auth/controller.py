"""Controller de Autenticação (Login/Logout)."""

from fastapi import Response, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import AuthService
from utils.logging import get_logger
from utils.settings import settings

logger = get_logger("auth_controller")

security = HTTPBearer(auto_error=False)


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

    response.delete_cookie(
        key="session_id",
        path="/",
        samesite="lax",
        secure=settings.secure_cookies,
        httponly=True,
    )
    return {"message": "Logout realizado"}


def get_current_user(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Função híbrida para autenticação via cookie OU Bearer token.

    Tenta autenticar nesta ordem:
    1. Session cookie
    2. Bearer token no header Authorization

    Retorna o nome do usuário autenticado ou levanta HTTPException se não autenticado.
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        username = AuthService.get_user_by_session(session_id)
        if username:
            logger.debug(f"Usuário autenticado via cookie: {username}")
            return username

    if credentials is not None and isinstance(
        credentials, HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            username = AuthService.authenticate_by_token(token)
            logger.debug(f"Usuário autenticado via Bearer token: {username}")
            return username
        except ValueError as e:
            logger.warning(f"Falha na autenticação via Bearer token: {e}")

    raise HTTPException(
        status_code=401,
        detail="Não autenticado. Use cookie ou header 'Authorization: Bearer <token>'",
    )
