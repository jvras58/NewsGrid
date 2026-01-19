from app.domain.status.repositories import ITaskStatusRepository
from app.infrastructure.cache.task_status_service import (
    delete_task_status,
    get_task_status,
    set_task_status,
    task_status_exists,
)


class RedisTaskStatusRepository(ITaskStatusRepository):
    def get_status(self, task_id: str) -> str | None:
        return get_task_status(task_id)

    def set_status(self, task_id: str, status: str) -> bool:
        return set_task_status(task_id, status)

    def delete_status(self, task_id: str) -> int:
        return delete_task_status(task_id)

    def exists(self, task_id: str) -> bool:
        return task_status_exists(task_id)
