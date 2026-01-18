from app.domain.auth.repositories import IAuthRepository
from app.domain.user.entities import UserEntity
from app.domain.user.repositories import IUserRepository
from utils.exceptions import BadRequestError
from utils.security import (
    create_access_token,
    verify_password,
)


class LoginUseCase:
    def __init__(self, auth_repo: IAuthRepository):
        self.auth_repo = auth_repo

    async def execute(self, username: str, password: str) -> str:
        auth_user = await self.auth_repo.get_by_username(username)
        if not auth_user or not verify_password(auth_user.hashed_password, password):
            raise BadRequestError("Credenciais inválidas")
        return create_access_token(data={"sub": username})


class GetCurrentUserUseCase:
    def __init__(self, auth_repo: IAuthRepository, user_repo: IUserRepository):
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    async def execute(self, username: str) -> UserEntity:
        auth_user = await self.auth_repo.get_by_username(username)
        if not auth_user:
            raise BadRequestError("Usuário não encontrado")
        full_user = await self.user_repo.get_by_username(username)
        return full_user
