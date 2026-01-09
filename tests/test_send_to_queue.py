from unittest.mock import patch, Mock
from utils.send_to_queue import send_to_queue


@patch("utils.send_to_queue.get_rabbitmq_connection")
def test_send_to_queue(mock_connection):
    mock_ch = Mock()
    mock_conn = Mock()
    mock_conn.channel.return_value = mock_ch
    mock_connection.return_value = mock_conn
    send_to_queue("test_queue", {"key": "value"})
    mock_ch.basic_publish.assert_called_once()
    mock_conn.close.assert_called_once()
