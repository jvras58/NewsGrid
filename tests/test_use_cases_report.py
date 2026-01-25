from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.report.use_cases import GetReportUseCase, RequestAnalysisUseCase


def test_request_analysis_use_case_success(mock_redis, mock_rabbitmq):
    cache_repo = MagicMock()
    cache_repo.get_cached_report.return_value = None
    task_repo = MagicMock()
    send_use_case = MagicMock()
    use_case = RequestAnalysisUseCase(cache_repo, task_repo, send_use_case)
    result = use_case.execute("IA", 1)
    assert "task_id" in result


@pytest.mark.asyncio
async def test_get_report_use_case_success(mock_redis):
    repo = AsyncMock()
    repo.get_report_by_task_id.return_value = AsyncMock(task_id="123", owner_id=1)
    use_case = GetReportUseCase(repo)
    report = await use_case.execute(None, "123", 1)
    assert report.task_id == "123"
