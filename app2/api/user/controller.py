from fastapi import HTTPException

from app2.api.user.schemas import UserCreate, UserDetailResponse, UserResponse
from app2.core.container import Container

container = Container()


async def create_user_logic(request: UserCreate) -> UserResponse:
    use_case = container.create_user_use_case()
    try:
        entity = await use_case.execute(
            request.username, request.email, request.password
        )
        return UserResponse.from_entity(entity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


async def list_users_logic() -> list[UserResponse]:
    use_case = container.list_users_use_case()
    try:
        entities = await use_case.execute()
        return [UserResponse.from_entity(e) for e in entities]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def get_user_logic(user_id: int) -> UserDetailResponse:
    use_case = container.get_user_by_id_use_case()
    try:
        entity = await use_case.execute(user_id)
        return UserDetailResponse.from_entity(entity)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
