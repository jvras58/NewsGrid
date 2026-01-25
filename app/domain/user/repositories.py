from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.entities import UserEntity


class IUserRepository(ABC):
    """Interface (Porta) para persistência de usuários."""

    @abstractmethod
    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> UserEntity | None:
        pass

    @abstractmethod
    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> UserEntity | None:
        pass

    @abstractmethod
    async def save(self, session: AsyncSession, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def list_all(self, session: AsyncSession) -> list[UserEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, user_id: int) -> UserEntity | None:
        pass
