from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import AuthEntity
from app.domain.auth.repositories import IAuthRepository
from app.domain.user.entities import UserEntity
from app.models.user import User as UserModel


class SQLAuthRepository(IAuthRepository):
    def _to_entity(self, model: UserModel) -> AuthEntity:
        return AuthEntity(
            id=model.id,
            username=model.username,
            hashed_password=model.hashed_password,
        )

    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> AuthEntity | None:
        result = await session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> UserEntity | None:
        result = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
