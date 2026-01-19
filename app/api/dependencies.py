"""
Dependencies para FastAPI.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.container import Container
from app.core.database import get_db
from app.domain.user.entities import UserEntity
from app.models import User
from app.services.rate_limit_service import check_rate_limit, get_user_limit
from utils.security import extract_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
container = Container()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserEntity:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = extract_username(token)
        if not username:
            raise credentials_exception
        use_case = container.get_current_user_use_case()
        return await use_case.execute(session, username)
    except PyJWTError:
        raise credentials_exception from credentials_exception


async def get_current_username(user: Annotated[User, Depends(get_current_user)]) -> str:
    """
    Dependency para obter o username do usuário autenticado.
    """
    return user.username


def get_rate_limit_dependency():
    """
    Dependency para rate limiting.
    """

    async def check_rate_limit_dep(
        request: Request, username: Annotated[str, Depends(get_current_username)]
    ):
        limit = get_user_limit(username)
        allowed, count, reset_in = check_rate_limit(username, limit)
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Limit: {limit}/min. Current: {count}. Reset in {reset_in}s",
            )
        return True

    return check_rate_limit_dep
