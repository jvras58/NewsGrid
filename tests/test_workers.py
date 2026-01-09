import json
from unittest.mock import Mock, patch
from app.workers.worker_researcher import ResearchWorker
from app.workers.worker_analyst import AnalystWorker


@patch("utils.broker.get_rabbitmq_connection")
@patch("app.workers.worker_researcher.ResearchAgent")
def test_research_worker_init(mock_agent_class, mock_connection):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent
    worker = ResearchWorker()
    assert worker.queue_name == "queue_research"
    assert worker.agent == mock_agent


@patch("utils.broker.get_rabbitmq_connection")
@patch("app.workers.worker_researcher.ResearchAgent")
@patch("app.workers.worker_researcher.send_to_queue")
def test_research_worker_process_message(mock_send, mock_agent_class, mock_connection):
    mock_agent = Mock()
    mock_agent.run.return_value = Mock(content="Mocked research")
    mock_agent_class.return_value = mock_agent
    worker = ResearchWorker()
    ch = Mock()
    method = Mock()
    properties = Mock()
    body = json.dumps({"topic": "Test", "task_id": "123"}).encode()
    worker.process_message(ch, method, properties, body)
    mock_send.assert_called_once_with(
        "queue_analysis",
        {"task_id": "123", "topic": "Test", "raw_research": "Mocked research"},
    )
    ch.basic_ack.assert_called_once()


@patch("utils.broker.get_rabbitmq_connection")
@patch("app.workers.worker_analyst.AnalystAgent")
@patch("app.workers.worker_analyst.save_report")
def test_analyst_worker_process_message(mock_save, mock_agent_class, mock_connection):
    mock_agent = Mock()
    mock_agent.run.return_value = Mock(content="Mocked report")
    mock_agent_class.return_value = mock_agent
    worker = AnalystWorker()
    ch = Mock()
    method = Mock()
    properties = Mock()
    body = json.dumps(
        {"topic": "Test", "raw_research": "Data", "task_id": "123"}
    ).encode()
    worker.process_message(ch, method, properties, body)
    mock_save.assert_called_once_with("123", "Test", "Mocked report")
    ch.basic_ack.assert_called_once()
