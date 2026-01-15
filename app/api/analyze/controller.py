"""
Lógica de negócio para requisições de análise.
"""

import uuid

from app.services.report_cache_service import get_cached_report, make_cache_key
from utils.logging import get_logger
from utils.send_to_queue import send_to_queue

logger = get_logger("analyze_controller")


def request_analysis_logic(topic: str, username: str = None):
    task_id = str(uuid.uuid4())
    logger.info(f"Iniciando análise: {topic} | User: {username} | Task ID: {task_id}")

    cache_key = make_cache_key(topic)
    cached_report = get_cached_report(cache_key)
    if cached_report:
        logger.info(f"Cache hit para tópico: {topic}")
        return {"status": "cached", "report": cached_report}

    payload = {"task_id": task_id, "topic": topic, "user_id": username}

    try:
        send_to_queue("queue_research", payload)
        logger.info(f"Análise enfileirada com sucesso para task_id: {task_id}")
        return {"status": "Processamento iniciado", "task_id": task_id}
    except Exception as e:
        logger.error(f"Falha ao enfileirar análise para tópico {topic}: {str(e)}")
        return {"status": "Falha ao iniciar o processamento", "error": str(e)}
