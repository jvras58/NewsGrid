"""Controller de Autenticação (JWT + OAuth2)."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.services.auth_service_sql import AuthServiceSQL
from utils.logging import get_logger
from utils.security import create_access_token, extract_username

logger = get_logger("auth_controller")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def login(username: str, password: str, session: AsyncSession) -> str:
    """
    Valida as credenciais (User + Password) e retorna o JWT.

    Agora consulta Postgres para usuários e verifica senha.
    """

    user = await AuthServiceSQL.get_user_by_username(session, username)
    if not user or not AuthServiceSQL.verify_password(user.hashed_password, password):
        raise ValueError("Credenciais inválidas")
    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"JWT gerado para: {user.username}")
    return access_token


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Valida o Token JWT nas requisições protegidas.

    Args:
        token: Token JWT extraído do header Authorization.

    Returns:
        User: Objeto do usuário autenticado.

    Raises:
        HTTPException: Se o token for inválido, expirado ou usuário revogado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = extract_username(token)
        if not username:
            raise credentials_exception
        user = await AuthServiceSQL.get_user_by_username(session, username)
        if not user:
            raise credentials_exception
    except PyJWTError as e:
        raise credentials_exception from e
    return user
