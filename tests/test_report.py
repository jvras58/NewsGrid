import json
from unittest.mock import patch, Mock
from app.services.report_service import ReportService


@patch("app.services.report_service.get_redis_client")
def test_save_report(mock_get_client):
    mock_client = Mock()
    mock_pipeline = Mock()
    mock_client.pipeline.return_value = mock_pipeline
    mock_get_client.return_value = mock_client
    ReportService.save("123", "Test Topic", "Content")
    mock_pipeline.set.assert_called_once_with(
        "report:123",
        json.dumps(
            {
                "task_id": "123",
                "topic": "Test Topic",
                "content": "Content",
                "owner": None,
            }
        ),
    )
    mock_pipeline.execute.assert_called_once()


@patch("app.services.report_service.get_redis_client")
def test_get_report_found(mock_get_client):
    mock_client = Mock()
    mock_client.get.return_value = json.dumps(
        {"task_id": "123", "topic": "Test", "content": "Data", "owner": None}
    )
    mock_get_client.return_value = mock_client
    result = ReportService.get_by_id("123")
    assert result == {
        "task_id": "123",
        "topic": "Test",
        "content": "Data",
        "owner": None,
    }
    mock_client.get.assert_called_once_with("report:123")


@patch("app.services.report_service.get_redis_client")
def test_get_report_not_found(mock_get_client):
    mock_client = Mock()
    mock_client.get.return_value = None
    mock_get_client.return_value = mock_client
    try:
        ReportService.get_by_id("123")
        assert False, "Deveria ter gerado um ValueError."
    except ValueError as e:
        assert str(e) == "Relatório não encontrado"
    mock_client.get.assert_called_once_with("report:123")


@patch("app.services.report_service.get_redis_client")
def test_get_report_access_denied(mock_get_client):
    mock_client = Mock()
    mock_client.get.return_value = json.dumps(
        {"task_id": "123", "topic": "Test", "content": "Data", "owner": "user1"}
    )
    mock_get_client.return_value = mock_client
    try:
        ReportService.get_by_id("123", user_id="user2")
        assert False, "Deveria ter gerado um ValueError."
    except ValueError as e:
        assert str(e) == "Acesso negado ao relatório"


@patch("app.services.report_service.get_redis_client")
def test_list_by_user(mock_get_client):
    mock_client = Mock()
    mock_client.smembers.return_value = ["report1", "report2"]
    mock_get_client.return_value = mock_client
    result = ReportService.list_by_user("user1")
    assert result == ["report1", "report2"]
    mock_client.smembers.assert_called_once_with("user:user1:reports")
