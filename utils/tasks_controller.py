from utils.redis_client import get_redis_client
from utils.settings import settings


def set_task_status(task_id: str, status: str) -> bool:
    """Define o status de uma tarefa no Redis com TTL de 24 horas.

    Args:
        task_id (str): ID da tarefa
        status (str): Status da tarefa (RESEARCHING, ANALYZING, COMPLETED, FAILED)

    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário
    """
    client = get_redis_client()
    key = settings.task_status_key_pattern.format(task_id=task_id)
    return client.setex(key, settings.task_status_ttl_seconds, status)


def get_task_status(task_id: str) -> str | None:
    """Obtém o status de uma tarefa do Redis.

    Args:
        task_id (str): ID da tarefa

    Returns:
        str | None: Status da tarefa ou None se não encontrado
    """
    client = get_redis_client()
    key = settings.task_status_key_pattern.format(task_id=task_id)
    return client.get(key)


def delete_task_status(task_id: str) -> int:
    """Remove o status de uma tarefa do Redis.

    Args:
        task_id (str): ID da tarefa

    Returns:
        int: Número de chaves removidas (0 ou 1)
    """
    client = get_redis_client()
    key = settings.task_status_key_pattern.format(task_id=task_id)
    return client.delete(key)


def get_all_task_statuses() -> dict[str, str]:
    """Obtém todos os status de tarefas do Redis.

    Returns:
        dict[str, str]: Dicionário com task_id como chave e status como valor
    """
    client = get_redis_client()
    keys = client.keys("task:*")
    if not keys:
        return {}
    statuses = client.mget(keys)
    return {
        key.split(":", 1)[1]: status
        for key, status in zip(keys, statuses, strict=True)
        if status
    }


def task_status_exists(task_id: str) -> bool:
    """Verifica se o status de uma tarefa existe no Redis.

    Args:
        task_id (str): ID da tarefa

    Returns:
        bool: True se existe, False caso contrário
    """
    client = get_redis_client()
    key = settings.task_status_key_pattern.format(task_id=task_id)
    return client.exists(key) == 1
