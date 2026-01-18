from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskStatusEntity:
    """Entidade de domínio pura para Status de Tarefa."""

    task_id: str
    status: str
    created_at: datetime | None = None

    def validate(self):
        """Validações básicas de domínio."""
        if not self.task_id:
            raise ValueError("Task ID é obrigatório")
        if not self.status:
            raise ValueError("Status é obrigatório")
