import json
from unittest.mock import patch, Mock
from utils.reporting import save_report, get_report


@patch("utils.reporting.get_redis_client")
def test_save_report(mock_get_client):
    mock_client = Mock()
    mock_get_client.return_value = mock_client
    save_report("123", "Test Topic", "Content")
    mock_client.set.assert_called_once_with(
        "report:123",
        json.dumps({"task_id": "123", "topic": "Test Topic", "content": "Content"}),
        ex=86400,
    )


@patch("utils.reporting.get_redis_client")
def test_get_report_found(mock_get_client):
    mock_client = Mock()
    mock_client.get.return_value = json.dumps(
        {"task_id": "123", "topic": "Test", "content": "Data"}
    )
    mock_get_client.return_value = mock_client
    result = get_report("123")
    assert result == {"task_id": "123", "topic": "Test", "content": "Data"}
    mock_client.get.assert_called_once_with("report:123")


@patch("utils.reporting.get_redis_client")
def test_get_report_not_found(mock_get_client):
    mock_client = Mock()
    mock_client.get.return_value = None
    mock_get_client.return_value = mock_client
    result = get_report("123")
    assert result is None
    mock_client.get.assert_called_once_with("report:123")
