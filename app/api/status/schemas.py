from datetime import datetime

from pydantic import BaseModel


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    created_at: datetime | None = None
