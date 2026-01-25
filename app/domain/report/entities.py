from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReportEntity:
    """Entidade de domínio pura para Relatório."""

    id: int | None
    task_id: str
    owner_id: int
    topic: str
    content: str | None
    created_at: datetime

    def validate(self):
        """Validações básicas de domínio."""
        if not self.task_id:
            raise ValueError("Task ID é obrigatório")
        if not self.topic:
            raise ValueError("Topic é obrigatório")
        if not self.owner_id:
            raise ValueError("Owner ID é obrigatório")
