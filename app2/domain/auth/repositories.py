from abc import ABC, abstractmethod

from app2.domain.user.entities import UserEntity


class IAuthRepository(ABC):
    """Interface (Porta) para Autenticação."""

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        pass
