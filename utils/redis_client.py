"""
Função Utilitária para conexão com Redis.
"""

import redis
from utils.settings import settings


def get_redis_client():
    """Estabelece e retorna uma conexão com o Redis.

    Args:
        None
    Returns:
        redis.Redis: Cliente Redis conectado.
    """
    client = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
    )
    if settings.redis_password:
        client.auth(settings.redis_password)
    return client
