from abc import ABC, abstractmethod


class IRateLimitRepository(ABC):
    @abstractmethod
    def check_rate_limit(self, identifier: str, limit: int) -> tuple[bool, int, int]:
        pass

    @abstractmethod
    def get_user_limit(self, username: str) -> int:
        pass
