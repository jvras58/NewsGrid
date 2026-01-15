# from unittest.mock import Mock, patch


# @patch("app.api.analyze.controller.send_to_queue")
# def test_request_analysis_success(mock_send, authenticated_client):
#     mock_send.return_value = None
#     response = authenticated_client.post(
#         "/api/v1/analyze/", json={"topic": "Test Topic"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "task_id" in data
#     assert data["status"] == "Processamento iniciado"
#     mock_send.assert_called_once()


# @patch("app.api.analyze.controller.send_to_queue")
# def test_request_analysis_failure(mock_send, authenticated_client):
#     mock_send.side_effect = Exception("Queue error")
#     response = authenticated_client.post(
#         "/api/v1/analyze/", json={"topic": "Test Topic"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "Falha ao iniciar o processamento"
#     assert "error" in data


# @patch("app.api.analyze.controller.ReportServiceSQL.get_report_by_task_id")
# def test_get_analysis_report_success(mock_get, authenticated_client, mock_username):
#     mock_report = Mock()
#     mock_report.task_id = "test_task_id"
#     mock_report.topic = "Test Topic"
#     mock_report.content = "Test content"
#     mock_report.user_id = mock_username
#     mock_get.return_value = mock_report
#     response = authenticated_client.get("/api/v1/analyze/report/test_task_id")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["task_id"] == "test_task_id"
#     assert data["topic"] == "Test Topic"
#     assert data["content"] == "Test content"
#     assert data["owner"] == mock_username
#     mock_get.assert_called_once()


# @patch("app.api.analyze.controller.ReportServiceSQL.get_report_by_task_id")
# def test_get_analysis_report_not_found(mock_get, authenticated_client):
#     mock_get.return_value = None
#     response = authenticated_client.get("/api/v1/analyze/report/test_task_id")
#     assert response.status_code == 404
#     data = response.json()
#     assert "detail" in data
#     assert data["detail"] == "Relatório não encontrado"


# @patch("app.api.analyze.controller.ReportServiceSQL.list_reports")
# def test_list_my_reports_success(mock_list, authenticated_client, mock_username):
#     mock_report1 = Mock()
#     mock_report1.task_id = "task1"
#     mock_report2 = Mock()
#     mock_report2.task_id = "task2"
#     mock_list.return_value = ([mock_report1, mock_report2], 2)
#     response = authenticated_client.get("/api/v1/analyze/my-reports")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["user"] == mock_username
#     assert data["reports"] == ["task1", "task2"]
#     mock_list.assert_called_once()


# @patch("app.api.analyze.controller.ReportServiceSQL.list_reports")
# def test_list_my_reports_error(mock_list, authenticated_client):
#     mock_list.side_effect = Exception("Erro ao listar")
#     response = authenticated_client.get("/api/v1/analyze/my-reports")
#     assert response.status_code == 400
#     data = response.json()
#     assert "detail" in data
#     assert data["detail"] == "Erro ao listar"
