from app.domain.report.repositories import IReportRepository
from app.domain.status.entities import TaskStatusEntity
from app.domain.status.repositories import ITaskStatusRepository
from utils.exceptions import BadRequestError


class GetTaskStatusUseCase:
    def __init__(
        self, task_status_repo: ITaskStatusRepository, report_repo: IReportRepository
    ):
        self.task_status_repo = task_status_repo
        self.report_repo = report_repo

    async def execute(self, task_id: str) -> TaskStatusEntity:
        status = self.task_status_repo.get_status(task_id)
        if not status:
            raise BadRequestError("Tarefa não encontrada ou expirada")

        report = await self.report_repo.get_report_by_task_id(task_id)
        created_at = report.get("created_at") if report else None

        return TaskStatusEntity(task_id=task_id, status=status, created_at=created_at)
