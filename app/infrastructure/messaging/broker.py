"""
Função Utilitária para conexão com RabbitMQ.
"""

import pika

from utils.settings import settings


def get_rabbitmq_connection():
    """Estabelece e retorna uma conexão com o RabbitMQ.

    Args:
        None
    Returns:
        pika.BlockingConnection: Conexão estabelecida com o RabbitMQ.
    """
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            credentials=pika.PlainCredentials(
                settings.rabbitmq_user, settings.rabbitmq_password
            ),
        )
    )
