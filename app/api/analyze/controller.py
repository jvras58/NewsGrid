"""
Lógica de negócio para requisições de análise.
"""

from utils.send_to_queue import send_to_queue
import uuid


def request_analysis_logic(topic: str):
    task_id = str(uuid.uuid4())
    payload = {"task_id": task_id, "topic": topic}
    try:
        send_to_queue("queue_research", payload)
        return {"status": "Processamento iniciado", "task_id": task_id}
    except Exception as e:
        return {"status": "Falha ao iniciar o processamento", "error": str(e)}
