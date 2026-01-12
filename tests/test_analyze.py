from unittest.mock import patch


@patch("app.api.analyze.controller.send_to_queue")
def test_request_analysis_success(mock_send, client):
    mock_send.return_value = None
    response = client.post("/api/v1/analyze/?topic=Test%20Topic")
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "Processamento iniciado"
    mock_send.assert_called_once()


@patch("app.api.analyze.controller.send_to_queue")
def test_request_analysis_failure(mock_send, client):
    mock_send.side_effect = Exception("Queue error")
    response = client.post("/api/v1/analyze/?topic=Test%20Topic")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Falha ao iniciar o processamento"
    assert "error" in data


@patch("app.services.report_service.ReportService.get_by_id")
def test_get_analysis_report_success(mock_get, client, mock_username):
    mock_report = {
        "task_id": "test_task_id",
        "topic": "Test Topic",
        "content": "Test content",
        "owner": mock_username,
    }
    mock_get.return_value = mock_report
    response = client.get("/api/v1/analyze/report/test_task_id")
    assert response.status_code == 200
    data = response.json()
    assert data == mock_report
    mock_get.assert_called_once_with("test_task_id", user_id=mock_username)


@patch("app.services.report_service.ReportService.get_by_id")
def test_get_analysis_report_not_found(mock_get, client):
    mock_get.side_effect = ValueError("Relatório não encontrado")
    response = client.get("/api/v1/analyze/report/test_task_id")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Relatório não encontrado"


@patch("app.services.report_service.ReportService.list_by_user")
def test_list_my_reports_success(mock_list, client, mock_username):
    mock_list.return_value = ["task1", "task2"]
    response = client.get("/api/v1/analyze/my-reports")
    assert response.status_code == 200
    data = response.json()
    assert data["user"] == mock_username
    assert data["reports"] == ["task1", "task2"]
    mock_list.assert_called_once_with(mock_username)


@patch("app.services.report_service.ReportService.list_by_user")
def test_list_my_reports_error(mock_list, client):
    mock_list.side_effect = ValueError("Erro ao listar")
    response = client.get("/api/v1/analyze/my-reports")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Erro ao listar"
