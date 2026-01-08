"""
Envio de mensagens para a fila RabbitMQ.
"""

import pika
import json
from utils.settings import settings


def send_to_queue(queue_name, data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            credentials=pika.PlainCredentials(
                settings.rabbitmq_user, settings.rabbitmq_password
            ),
        )
    )
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
    connection.close()
