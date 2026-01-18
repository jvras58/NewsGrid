from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.entities import UserEntity
from app.domain.user.repositories import IUserRepository
from app.models.user import (
    User as UserModel,
)


class SQLUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            created_at=model.created_at,
        )

    def _to_model(self, entity: UserEntity) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            created_at=entity.created_at,
        )

    async def get_by_username(self, username: str) -> UserEntity | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> UserEntity | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def save(self, user: UserEntity) -> UserEntity:
        model = self._to_model(user)
        self.session.add(model)
        try:
            await self.session.commit()
            await self.session.refresh(model)
            return self._to_entity(model)
        except IntegrityError as err:
            await self.session.rollback()
            raise ValueError("Erro ao salvar usuário (possível duplicata)") from err

    async def list_all(self) -> list[UserEntity]:
        result = await self.session.execute(select(UserModel))
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
