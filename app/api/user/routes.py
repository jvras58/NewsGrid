from fastapi import APIRouter, Depends

from app.api.auth.controller import get_current_user
from app.api.user.controller import (
    create_user_logic,
    list_users_logic,
)
from app.api.user.schemas import UserCreate, UserResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return create_user_logic(user.username, user.email, user.password)


@router.get("/")
async def list_users():
    return list_users_logic()
