"""Controller de Autenticação (JWT + OAuth2)."""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.services.auth_service import AuthService
from utils.security import create_access_token, extract_username
from utils.logging import get_logger

logger = get_logger("auth_controller")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def login_logic(username: str, token_senha: str):
    """
    Valida as credenciais (User + Token) e retorna o JWT.

    Args:
        username: Nome do usuário.
        token_senha: Token de acesso do usuário (funciona como senha).

    Returns:
        dict: Contendo access_token e token_type.

    Raises:
        HTTPException: Se as credenciais forem inválidas.
    """
    try:
        user_do_token = AuthService.authenticate_by_token(token_senha)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user_do_token != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não pertence a este usuário",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": username})
    logger.info(f"JWT gerado para: {username}")
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Valida o Token JWT nas requisições protegidas.

    Args:
        token: Token JWT extraído do header Authorization.

    Returns:
        str: Username do usuário autenticado.

    Raises:
        HTTPException: Se o token for inválido ou expirado.
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
    except JWTError:
        raise credentials_exception
    return username
