"""
Lógica de negócio para requisições de análise.
"""

import uuid

from app.services.report_cache_service import get_cached_report, make_cache_key
from app.services.task_status_service import task_status_service
from utils.logging import get_logger
from utils.send_to_queue import send_to_queue

logger = get_logger("analyze_controller")


def request_analysis_logic(topic: str, user_id: int):
    """
    Lógica para iniciar análise de tópico.

    Args:
        topic (str): Tópico para análise.
        user_id (int): ID do usuário autenticado (de Postgres).

    Returns:
        dict: Resposta com status e task_id ou relatório cached.
    """
    logger.info(f"Iniciando análise: {topic} | User ID: {user_id}")

    cache_key = make_cache_key(topic)
    cached_report = get_cached_report(cache_key)
    if cached_report:
        logger.info(f"Cache hit para tópico: {topic}")
        return {"status": "cached", "report": cached_report}

    task_id = str(uuid.uuid4())
    task_status_service.set_researching(task_id)

    payload = {"task_id": task_id, "topic": topic, "user_id": str(user_id)}

    try:
        send_to_queue("queue_research", payload)
        logger.info(f"Análise enfileirada com sucesso para task_id: {task_id}")
        return {"status": "Processamento iniciado", "task_id": task_id}
    except Exception as e:
        logger.error(f"Falha ao enfileirar análise para tópico {topic}: {str(e)}")
        task_status_service.set_failed(task_id)
        return {"status": "Falha ao iniciar o processamento", "error": str(e)}
