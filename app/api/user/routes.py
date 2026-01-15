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

Session = Annotated[AsyncSession, Depends(get_db)]
get_current_user_dep = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session,
    current_user=get_current_user_dep,
):
    return await create_user_logic(user.username, user.email, user.password, db)


@router.get("/")
async def list_users(
    db: Session,
    current_user=get_current_user_dep,
):
    return await list_users_logic(db)
