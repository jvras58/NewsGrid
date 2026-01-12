"""
Lógica de negócio para requisições de análise.
"""

from utils.send_to_queue import send_to_queue
from utils.logging import get_logger
import uuid

logger = get_logger("analyze_controller")


def request_analysis_logic(topic: str, username: str = None):
    task_id = str(uuid.uuid4())
    logger.info(f"Iniciando análise: {topic} | User: {username} | Task ID: {task_id}")

    payload = {"task_id": task_id, "topic": topic, "user_id": username}

    try:
        send_to_queue("queue_research", payload)
        logger.info(f"Análise enfileirada com sucesso para task_id: {task_id}")
        return {"status": "Processamento iniciado", "task_id": task_id}
    except Exception as e:
        logger.error(f"Falha ao enfileirar análise para tópico {topic}: {str(e)}")
        return {"status": "Falha ao iniciar o processamento", "error": str(e)}
