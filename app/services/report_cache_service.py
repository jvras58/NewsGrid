"""
Serviço para cache de relatórios por tópico no Redis.
"""

import hashlib
import json
from typing import Any

from utils.redis_client import get_redis_client
from utils.settings import settings


def make_cache_key(topic: str, params: dict[str, Any] | None = None) -> str:
    """
    Cria chave de cache normalizada para tópico.

    Args:
        topic: Tópico da pesquisa.
        params: Parâmetros adicionais (opcional).

    Returns:
        Chave hashada.
    """
    normalized_topic = topic.lower().strip()
    key_data = f"topic:{normalized_topic}"
    if params:
        sorted_params = json.dumps(params, sort_keys=True)
        key_data += f":{sorted_params}"
    return f"report_cache:{hashlib.sha256(key_data.encode()).hexdigest()}"


def get_cached_report(cache_key: str) -> dict[str, Any] | None:
    """
    Obtém relatório do cache.

    Args:
        cache_key: Chave do cache.

    Returns:
        Relatório ou None.
    """
    client = get_redis_client()
    data = client.get(cache_key)
    if data:
        return json.loads(data)
    return None


def set_cached_report(cache_key: str, report: dict[str, Any]) -> bool:
    """
    Salva relatório no cache com TTL.

    Args:
        cache_key: Chave do cache.
        report: Dados do relatório.

    Returns:
        True se sucesso.
    """
    client = get_redis_client()
    return client.setex(
        cache_key, settings.report_cache_ttl_seconds, json.dumps(report)
    )
