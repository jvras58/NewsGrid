"""
Envio de mensagens para a fila RabbitMQ.
"""

import pika
import json
from utils.broker import get_rabbitmq_connection
from utils.logging import get_logger

logger = get_logger(__name__)


def send_to_queue(queue_name, data):
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
    finally:
        connection.close()
