from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app2.domain.auth.entities import AuthEntity
from app2.domain.auth.repositories import IAuthRepository
from app2.models.user import User as UserModel


class SQLAuthRepository(IAuthRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: UserModel) -> AuthEntity:
        return AuthEntity(
            id=model.id,
            username=model.username,
            hashed_password=model.hashed_password,
        )

    async def get_by_username(self, username: str) -> AuthEntity | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
