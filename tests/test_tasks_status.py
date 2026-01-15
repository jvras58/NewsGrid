from unittest.mock import patch

from app.services.task_status_service import TaskStatusService, task_status_service
from utils.settings import settings


@patch("app.services.task_status_service.set_task_status")
def test_set_researching(mock_set_task_status):
    mock_set_task_status.return_value = True
    result = TaskStatusService.set_researching("123")
    assert result is True
    mock_set_task_status.assert_called_once_with(
        "123", settings.task_status_researching
    )


@patch("app.services.task_status_service.set_task_status")
def test_set_analyzing(mock_set_task_status):
    mock_set_task_status.return_value = True
    result = TaskStatusService.set_analyzing("123")
    assert result is True
    mock_set_task_status.assert_called_once_with("123", settings.task_status_analyzing)


@patch("app.services.task_status_service.set_task_status")
def test_set_completed(mock_set_task_status):
    mock_set_task_status.return_value = True
    result = TaskStatusService.set_completed("123")
    assert result is True
    mock_set_task_status.assert_called_once_with("123", settings.task_status_completed)


@patch("app.services.task_status_service.set_task_status")
def test_set_failed(mock_set_task_status):
    mock_set_task_status.return_value = True
    result = TaskStatusService.set_failed("123")
    assert result is True
    mock_set_task_status.assert_called_once_with("123", settings.task_status_failed)


@patch("app.services.task_status_service.get_task_status")
def test_get_status(mock_get_task_status):
    mock_get_task_status.return_value = "COMPLETED"
    result = TaskStatusService.get_status("123")
    assert result == "COMPLETED"
    mock_get_task_status.assert_called_once_with("123")


@patch("app.services.task_status_service.get_task_status")
def test_is_researching_true(mock_get_task_status):
    mock_get_task_status.return_value = settings.task_status_researching
    result = TaskStatusService.is_researching("123")
    assert result is True


@patch("app.services.task_status_service.get_task_status")
def test_is_researching_false(mock_get_task_status):
    mock_get_task_status.return_value = "OTHER"
    result = TaskStatusService.is_researching("123")
    assert result is False


@patch("app.services.task_status_service.get_task_status")
def test_is_analyzing_true(mock_get_task_status):
    mock_get_task_status.return_value = settings.task_status_analyzing
    result = TaskStatusService.is_analyzing("123")
    assert result is True


@patch("app.services.task_status_service.get_task_status")
def test_is_analyzing_false(mock_get_task_status):
    mock_get_task_status.return_value = "OTHER"
    result = TaskStatusService.is_analyzing("123")
    assert result is False


@patch("app.services.task_status_service.get_task_status")
def test_is_completed_true(mock_get_task_status):
    mock_get_task_status.return_value = settings.task_status_completed
    result = TaskStatusService.is_completed("123")
    assert result is True


@patch("app.services.task_status_service.get_task_status")
def test_is_completed_false(mock_get_task_status):
    mock_get_task_status.return_value = "OTHER"
    result = TaskStatusService.is_completed("123")
    assert result is False


@patch("app.services.task_status_service.get_task_status")
def test_is_failed_true(mock_get_task_status):
    mock_get_task_status.return_value = settings.task_status_failed
    result = TaskStatusService.is_failed("123")
    assert result is True


@patch("app.services.task_status_service.get_task_status")
def test_is_failed_false(mock_get_task_status):
    mock_get_task_status.return_value = "OTHER"
    result = TaskStatusService.is_failed("123")
    assert result is False


@patch("app.services.task_status_service.task_status_exists")
def test_exists_true(mock_task_status_exists):
    mock_task_status_exists.return_value = True
    result = TaskStatusService.exists("123")
    assert result is True
    mock_task_status_exists.assert_called_once_with("123")


@patch("app.services.task_status_service.task_status_exists")
def test_exists_false(mock_task_status_exists):
    mock_task_status_exists.return_value = False
    result = TaskStatusService.exists("123")
    assert result is False


@patch("app.services.task_status_service.delete_task_status")
def test_delete(mock_delete_task_status):
    mock_delete_task_status.return_value = 1
    result = TaskStatusService.delete("123")
    assert result == 1
    mock_delete_task_status.assert_called_once_with("123")


@patch("app.services.task_status_service.get_all_task_statuses")
def test_get_all_statuses(mock_get_all_task_statuses):
    mock_get_all_task_statuses.return_value = {"123": "COMPLETED", "456": "FAILED"}
    result = TaskStatusService.get_all_statuses()
    assert result == {"123": "COMPLETED", "456": "FAILED"}
    mock_get_all_task_statuses.assert_called_once()


@patch("app.services.task_status_service.get_all_task_statuses")
def test_get_active_tasks(mock_get_all_task_statuses):
    mock_get_all_task_statuses.return_value = {
        "123": settings.task_status_researching,
        "456": settings.task_status_analyzing,
        "789": settings.task_status_completed,
    }
    result = TaskStatusService.get_active_tasks()
    assert set(result) == {"123", "456"}


@patch("app.services.task_status_service.get_all_task_statuses")
def test_get_completed_tasks(mock_get_all_task_statuses):
    mock_get_all_task_statuses.return_value = {
        "123": settings.task_status_completed,
        "456": settings.task_status_failed,
    }
    result = TaskStatusService.get_completed_tasks()
    assert result == ["123"]


@patch("app.services.task_status_service.get_all_task_statuses")
def test_get_failed_tasks(mock_get_all_task_statuses):
    mock_get_all_task_statuses.return_value = {
        "123": settings.task_status_completed,
        "456": settings.task_status_failed,
    }
    result = TaskStatusService.get_failed_tasks()
    assert result == ["456"]


def test_task_status_service_instance():
    assert isinstance(task_status_service, TaskStatusService)
