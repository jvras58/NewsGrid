"""
Implementação do broker de mensagens usando RabbitMQ.
"""

import json

import pika

from app.domain.exceptions import MessageSendError
from app.domain.messaging.repositories import IMessageBroker
from app.infrastructure.messaging.broker import get_rabbitmq_connection
from utils.logging import get_logger

logger = get_logger("RabbitMQBroker")


class RabbitMQBroker(IMessageBroker):
    def send_to_queue(self, queue_name: str, data: dict) -> None:
        """Envia uma mensagem para a fila RabbitMQ especificada.

        Args:
            queue_name (str): Nome da fila.
            data (Dict[str, Any]): Dados a serem enviados.

        Raises:
            MessageSendError: Se houver erro ao enviar a mensagem.
        """
        try:
            connection = get_rabbitmq_connection()
        except Exception as exc:
            data_summary = (
                str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
            )
            raise MessageSendError(
                f"Erro ao enviar para {queue_name}: {exc}",
                queue_name=queue_name,
                data_summary=data_summary,
            ) from exc

        try:
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)

            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(data),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            logger.info(f"Mensagem enviada para a fila {queue_name}")
        except Exception as exc:
            logger.error(
                "Erro ao enviar mensagem para a fila %s: %s",
                queue_name,
                exc,
                exc_info=True,
            )
            raise MessageSendError(f"Erro ao enviar para {queue_name}: {exc}") from exc
        finally:
            connection.close()
