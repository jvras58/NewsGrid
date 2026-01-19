from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.container import Container
from app.core.database import get_db
from app.domain.user.entities import (
    UserEntity,
)
from utils.security import extract_username

container = Container()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def login(username: str, password: str, session):
    use_case = container.login_use_case()
    try:
        return await use_case.execute(session, username, password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e)) from e


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
