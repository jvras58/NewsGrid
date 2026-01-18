from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.entities import UserEntity


class IAuthRepository(ABC):
    """Interface (Porta) para Autenticação."""

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
