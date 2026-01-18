from abc import ABC, abstractmethod

from app.domain.user.entities import UserEntity


class IUserRepository(ABC):
    """Interface (Porta) para persistência de usuários."""

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        pass

    @abstractmethod
    async def save(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def list_all(self) -> list[UserEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserEntity | None:
        pass
