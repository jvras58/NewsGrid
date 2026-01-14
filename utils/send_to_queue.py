"""
Envio de mensagens para a fila RabbitMQ.
"""

import json

import pika

from utils.broker import get_rabbitmq_connection
from utils.logging import get_logger

logger = get_logger("send_to_queue")


def send_to_queue(queue_name, data):
    """Envia uma mensagem para a fila RabbitMQ especificada.

    Args:
        queue_name (str): Nome da fila para onde a mensagem será enviada.
        data (dict): Dados a serem enviados na mensagem.
    Returns:
        None
    """
    connection = get_rabbitmq_connection()
    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )
        logger.info(f"Mensagem enviada para a fila {queue_name}")
    except Exception as exc:
        logger.error(
            "Erro ao enviar mensagem para a fila %s: %s",
            queue_name,
            exc,
            exc_info=True,
        )
        raise
    finally:
        connection.close()
