from datetime import datetime

from pydantic import BaseModel

from app2.domain.status.entities import TaskStatusEntity


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    created_at: datetime | None = None

    @classmethod
    def from_entity(cls, entity: TaskStatusEntity) -> "TaskStatusResponse":
        return cls(
            task_id=entity.task_id,
            status=entity.status,
            created_at=entity.created_at,
        )
