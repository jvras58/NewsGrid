from abc import ABC, abstractmethod
from typing import Any

from app.domain.report.entities import ReportEntity


class IReportRepository(ABC):
    """Interface (Porta) para persistência de relatórios (SQL)."""

    @abstractmethod
    async def create_report(
        self, task_id: str, owner_id: int, topic: str, content: str | None
    ) -> ReportEntity:
        pass

    @abstractmethod
    async def get_report_by_task_id(self, task_id: str) -> ReportEntity | None:
        pass

    @abstractmethod
    async def list_reports_by_owner(
        self, owner_id: int, topic_filter: str | None, page: int, per_page: int
    ) -> tuple[list[ReportEntity], int]:
        pass


class ICacheRepository(ABC):
    """Interface (Porta) para cache de relatórios (Redis)."""

    @abstractmethod
    def make_cache_key(self, topic: str, params: dict[str, Any] | None = None) -> str:
        pass

    @abstractmethod
    def get_cached_report(self, cache_key: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def set_cached_report(self, cache_key: str, report: dict[str, Any]) -> bool:
        pass
