"""
Função Utilitária para conexão com RabbitMQ.
"""

import pika
from utils.settings import settings


def get_rabbitmq_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            credentials=pika.PlainCredentials(
                settings.rabbitmq_user, settings.rabbitmq_password
            ),
        )
    )
