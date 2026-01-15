"""
Dependencies para FastAPI.
"""

from fastapi import Depends, HTTPException, Request

from app.services.rate_limit_service import check_rate_limit, get_user_limit


def get_rate_limit_dependency():
    """
    Dependency para rate limiting.
    """

    async def check_rate_limit_dep(
        request: Request, username: str = Depends(get_current_user_placeholder)
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


# TODO: Placeholder para get_current_user (adaptar do auth)
def get_current_user_placeholder(request: Request) -> str:
    # Simulação: pegar do header ou token
    return request.headers.get("X-Username", "anonymous")
