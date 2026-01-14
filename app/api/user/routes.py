from fastapi import APIRouter, Depends
from app.api.user.schemas import UserCreate, UserResponse
from app.api.user.controller import (
    create_user_logic,
    list_users_logic,
    revoke_user_logic,
)
from app.api.auth.controller import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return create_user_logic(user.username, user.token)


@router.get("/")
async def list_users():
    return list_users_logic()


@router.delete("/{username}")
async def revoke_user(username: str):
    return revoke_user_logic(username)
