import uuid
from typing import Any

from app.domain.report.entities import ReportEntity
from app.domain.report.repositories import ICacheRepository, IReportRepository
from app.domain.status.repositories import ITaskStatusRepository
from utils.exceptions import BadRequestError
from utils.send_to_queue import send_to_queue


class RequestAnalysisUseCase:
    def __init__(
        self, cache_repo: ICacheRepository, task_status_repo: ITaskStatusRepository
    ):
        self.cache_repo = cache_repo
        self.task_status_repo = task_status_repo

    def execute(self, topic: str, user_id: int) -> dict[str, Any]:
        cache_key = self.cache_repo.make_cache_key(topic)
        cached_report = self.cache_repo.get_cached_report(cache_key)
        if cached_report:
            return {"status": "cached", "report": cached_report}

        task_id = str(uuid.uuid4())
        self.task_status_repo.set_status(task_id, "RESEARCHING")

        payload = {"task_id": task_id, "topic": topic, "user_id": str(user_id)}
        try:
            send_to_queue("queue_research", payload)
            return {"status": "Processamento iniciado", "task_id": task_id}
        except Exception as e:
            self.task_status_repo.set_status(task_id, "FAILED")
            raise BadRequestError(f"Falha ao iniciar o processamento: {str(e)}") from e


class GetReportUseCase:
    def __init__(self, report_repo: IReportRepository):
        self.report_repo = report_repo

    async def execute(self, task_id: str, user_id: int) -> ReportEntity:
        report = await self.report_repo.get_report_by_task_id(task_id)
        if not report:
            raise BadRequestError("Relatório não encontrado")
        if report.owner_id != user_id:
            raise BadRequestError("Acesso negado ao relatório")
        return report


class ListMyReportsUseCase:
    def __init__(self, report_repo: IReportRepository):
        self.report_repo = report_repo

    async def execute(
        self, user_id: int, topic_filter: str | None, page: int, per_page: int
    ) -> tuple[list[str], int]:
        reports, total = await self.report_repo.list_reports_by_owner(
            user_id, topic_filter, page, per_page
        )
        task_ids = [report.task_id for report in reports]
        return task_ids, total


class ProcessResearchUseCase:
    def __init__(self, task_status_repo: ITaskStatusRepository):
        self.task_status_repo = task_status_repo

    def execute(
        self, task_id: str, topic: str, user_id: int, raw_research: str | None = None
    ) -> dict[str, Any]:
        self.task_status_repo.set_status(task_id, "RESEARCHING")
        if raw_research is None:
            raw_research = f"Dados brutos pesquisados para {topic}."
        return {
            "task_id": task_id,
            "topic": topic,
            "raw_research": raw_research,
            "user_id": user_id,
        }


class ProcessAnalysisUseCase:
    def __init__(
        self,
        report_repo: IReportRepository,
        cache_repo: ICacheRepository,
        task_status_repo: ITaskStatusRepository,
    ):
        self.report_repo = report_repo
        self.cache_repo = cache_repo
        self.task_status_repo = task_status_repo

    async def execute(
        self,
        task_id: str,
        topic: str,
        raw_research: str,
        user_id: int,
        final_report: str,
    ) -> None:
        self.task_status_repo.set_status(task_id, "ANALYZING")

        # Cria relatório com o final_report gerado
        await self.report_repo.create_report(task_id, user_id, topic, final_report)

        # Cache
        cache_key = self.cache_repo.make_cache_key(topic)
        self.cache_repo.set_cached_report(
            cache_key,
            {
                "task_id": task_id,
                "topic": topic,
                "content": final_report,
                "owner": user_id,
            },
        )

        self.task_status_repo.set_status(task_id, "COMPLETED")
