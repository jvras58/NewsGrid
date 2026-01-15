from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.controller import get_current_user
from app.api.user.controller import (
    create_user_logic,
    list_users_logic,
)
from app.api.user.schemas import UserCreate, UserResponse
from app.core.database import get_db
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    session: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await create_user_logic(user.username, user.email, user.password, session)


@router.get("/")
async def list_users(
    session: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await list_users_logic(session)
