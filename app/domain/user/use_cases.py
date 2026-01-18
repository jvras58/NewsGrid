from datetime import UTC, datetime

from app.domain.user.entities import UserEntity
from app.domain.user.repositories import IUserRepository
from utils.exceptions import BadRequestError
from utils.security import hash_password


class CreateUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, db, username: str, email: str, password: str) -> UserEntity:
        if not username or not email or not password:
            raise BadRequestError("Campos obrigatórios")
        if len(username) < 3:
            raise BadRequestError("Username deve ter pelo menos 3 caracteres")

        if await self.user_repo.get_by_username(db, username):
            raise BadRequestError("Username já existe")
        if await self.user_repo.get_by_email(db, email):
            raise BadRequestError("Email já existe")

        hashed = hash_password(password)
        user_entity = UserEntity(
            id=None,
            username=username,
            email=email,
            hashed_password=hashed,
            created_at=datetime.now(UTC),
        )
        user_entity.validate()
        return await self.user_repo.save(db, user_entity)


class ListUsersUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, db) -> list[UserEntity]:
        return await self.user_repo.list_all(db)


class GetUserByIdUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, db, user_id: int) -> UserEntity:
        user = await self.user_repo.get_by_id(db, user_id)
        if not user:
            raise BadRequestError("Usuário não encontrado")
        return user
