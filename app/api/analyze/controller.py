"""
Lógica de negócio para requisições de análise.
"""

from utils.send_to_queue import send_to_queue
import uuid


def request_analysis_logic(topic: str):
    task_id = str(uuid.uuid4())
    payload = {"task_id": task_id, "topic": topic}
    send_to_queue("queue_research", payload)
    return {"status": "Processing initiated", "task_id": task_id}
