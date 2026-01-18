from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth.controller import get_current_user
from app.api.user.controller import create_user_logic, get_user_logic, list_users_logic
from app.api.user.schemas import UserCreate, UserDetailResponse, UserResponse
from app.domain.user.entities import UserEntity

router = APIRouter()

get_current_user_dep = Annotated[UserEntity, Depends(get_current_user)]


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return await create_user_logic(user)


@router.get("/", response_model=list[UserResponse])
async def list_users(current_user: get_current_user_dep):
    return await list_users_logic()


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, current_user: get_current_user_dep):
    return await get_user_logic(user_id)
