from unittest.mock import MagicMock, patch

from app.infrastructure.workers.worker_researcher import ResearchWorker


def test_research_worker_run(mock_rabbitmq):
    with (
        patch(
            "app.infrastructure.workers.worker_researcher.ResearchAgent"
        ) as mock_agent,
        patch("app.infrastructure.workers.worker_researcher.json") as mock_json,
    ):
        worker = ResearchWorker()
        with (
            patch.object(worker.container, "process_research_use_case") as mock_process,
            patch.object(worker.container, "send_message_use_case") as mock_send,
            patch.object(worker.container, "task_status_repo") as mock_status_repo,
        ):
            mock_agent.return_value.run.return_value = MagicMock(
                content="Pesquisa concluída"
            )
            mock_json.loads.return_value = {"task_id": "123", "topic": "IA"}
            mock_process.return_value.execute.return_value = {"some": "data"}
            mock_send.return_value.execute = MagicMock()
            mock_status_repo.return_value.set_status = MagicMock()
            mock_ch = MagicMock()
            mock_method = MagicMock()
            mock_properties = MagicMock()
            body = b"dummy"
            worker.process_message(mock_ch, mock_method, mock_properties, body)
            mock_agent.return_value.run.assert_called_once()
