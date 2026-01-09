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
