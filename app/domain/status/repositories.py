from abc import ABC, abstractmethod


class ITaskStatusRepository(ABC):
    """Interface (Porta) para persistência de status de tarefas (Redis)."""

    @abstractmethod
    def get_status(self, task_id: str) -> str | None:
        pass

    @abstractmethod
    def set_status(self, task_id: str, status: str) -> bool:
        pass

    @abstractmethod
    def delete_status(self, task_id: str) -> int:
        pass

    @abstractmethod
    def exists(self, task_id: str) -> bool:
        pass
