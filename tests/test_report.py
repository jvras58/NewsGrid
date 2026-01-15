from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.services.report_service_sql import ReportServiceSQL


@pytest.mark.asyncio
@patch("app.services.report_service_sql.AsyncSession")
async def test_create_report_success(mock_session_class):
    mock_session = AsyncMock()
    mock_session_class.return_value = mock_session
    mock_session.add = Mock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    mock_report = Mock()
    mock_report.id = 1
    mock_session.refresh.side_effect = lambda r: setattr(r, "id", 1)

    result = await ReportServiceSQL.create_report(
        mock_session, "task123", 1, "Test Topic", "Content"
    )

    assert result == {"status": "created", "report_id": 1}
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.report_service_sql.AsyncSession")
async def test_create_report_failure(mock_session_class):
    mock_session = AsyncMock()
    mock_session_class.return_value = mock_session
    mock_session.add = Mock()
    mock_session.commit = AsyncMock(side_effect=Exception("DB error"))
    mock_session.rollback = AsyncMock()

    with pytest.raises(ValueError, match="Erro ao criar relatório"):
        await ReportServiceSQL.create_report(
            mock_session, "task123", 1, "Test Topic", "Content"
        )

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.report_service_sql.AsyncSession")
async def test_get_report_by_task_id_found(mock_session_class):
    mock_session = AsyncMock()
    mock_session_class.return_value = mock_session
    mock_result = Mock()
    mock_report = Mock()
    mock_report.task_id = "task123"
    mock_report.owner = Mock()
    mock_result.unique.return_value.scalar_one_or_none.return_value = mock_report
    mock_session.execute.return_value = mock_result

    result = await ReportServiceSQL.get_report_by_task_id(mock_session, "task123")

    assert result == mock_report
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.report_service_sql.AsyncSession")
async def test_get_report_by_task_id_not_found(mock_session_class):
    mock_session = AsyncMock()
    mock_session_class.return_value = mock_session
    mock_result = Mock()
    mock_result.unique.return_value.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    result = await ReportServiceSQL.get_report_by_task_id(mock_session, "task123")

    assert result is None


@pytest.mark.asyncio
@patch("app.services.report_service_sql.AsyncSession")
async def test_list_reports(mock_session_class):
    mock_session = AsyncMock()
    mock_session_class.return_value = mock_session
    mock_reports = [Mock(), Mock()]
    mock_result = Mock()
    mock_result.unique.return_value.scalars.return_value.all.return_value = mock_reports
    mock_session.execute.side_effect = [
        Mock(scalar=lambda: 2),
        mock_result,
    ]

    reports, total = await ReportServiceSQL.list_reports(mock_session, 1)

    assert reports == mock_reports
    assert total == 2
