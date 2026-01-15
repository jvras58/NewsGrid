"""
Serviço para rate limiting usando Redis com sliding window.
"""

import time

from utils.redis_client import get_redis_client

WINDOW_SECONDS = 60  # 1 minuto


def check_rate_limit(identifier: str, limit: int) -> tuple[bool, int, int]:
    """
    Verifica rate limit usando sliding window.

    Args:
        identifier: user ou IP.
        limit: limite de requests.

    Returns:
        (allowed, current_count, reset_in_seconds)
    """
    client = get_redis_client()
    key = f"rate_limit:{identifier}"
    now = time.time()
    window_start = now - WINDOW_SECONDS

    # Adicionar timestamp atual
    client.zadd(key, {str(now): now})
    # Remover timestamps antigos
    client.zremrangebyscore(key, "-inf", window_start)
    # Contar requests na janela
    count = client.zcard(key)
    # TTL para expirar automaticamente
    client.expire(key, WINDOW_SECONDS)

    allowed = count <= limit
    reset_in = int(WINDOW_SECONDS - (now - window_start))
    return allowed, count, reset_in


def get_user_limit(username: str) -> int:
    """
    Retorna limite baseado no usuário (simples: free=10, premium=100).
    """
    # Simulação: se username contém 'premium', 100, else 10
    if "premium" in username.lower():
        return 100
    return 10
