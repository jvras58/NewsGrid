"""
Dependencies para FastAPI.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, Request

from app.api.auth.controller import get_current_user
from app.models import User
from app.services.rate_limit_service import check_rate_limit, get_user_limit


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
