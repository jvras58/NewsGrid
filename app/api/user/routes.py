from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.api.user.controller import create_user_logic, get_user_logic, list_users_logic
from app.api.user.schemas import UserCreate, UserDetailResponse, UserResponse
from app.core.database import get_db
from app.domain.user.entities import UserEntity

router = APIRouter()

get_current_user_dep = Annotated[UserEntity, Depends(get_current_user)]
session = Annotated[AsyncSession, Depends(get_db)]


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: session):
    return await create_user_logic(user, db)


@router.get("/", response_model=list[UserResponse])
async def list_users(current_user: get_current_user_dep, db: session):
    return await list_users_logic(db)


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, current_user: get_current_user_dep, db: session):
    return await get_user_logic(user_id, db)
