"""
Módulo utilitário para funções de geração e salvamento de relatórios.
"""

import json
from utils.logging import get_logger
from utils.redis_client import get_redis_client

logger = get_logger("save_report")


def save_report(task_id: str, topic: str, report_content: str):
    """
    Salva o relatório gerado no Redis.

    Args:
        task_id (str): ID da tarefa associada ao relatório.
        topic (str): Tópico do relatório.
        report_content (str): Conteúdo do relatório a ser salvo.

    Returns:
        None
    """
    redis_client = get_redis_client()
    key = f"report:{task_id}"
    data = {"task_id": task_id, "topic": topic, "content": report_content}
    try:
        redis_client.set(key, json.dumps(data), ex=86400)
        logger.info(f"Relatório salvo no Redis com chave: {key}")
    except Exception as e:
        logger.error(f"Erro ao salvar relatório no Redis: {e}")


def get_report(task_id: str):
    """
    Recupera o relatório do Redis pelo task_id.

    Args:
        task_id (str): ID da tarefa do relatório.

    Returns:
        dict or None: Dados do relatório se encontrado, None caso contrário.
    """
    redis_client = get_redis_client()
    key = f"report:{task_id}"
    try:
        data_str = redis_client.get(key)
        if data_str:
            return json.loads(data_str)
        else:
            logger.warning(f"Relatório não encontrado no Redis para task_id: {task_id}")
            return None
    except Exception as e:
        logger.error(f"Erro ao recuperar relatório do Redis: {e}")
        return None
