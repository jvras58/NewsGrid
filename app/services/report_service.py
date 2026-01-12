"""Serviço para manipulação de relatórios no Redis."""

import json
from utils.redis_client import get_redis_client
from utils.logging import get_logger

logger = get_logger("report_service")


class ReportService:
    @staticmethod
    def save(task_id: str, topic: str, content: str, user_id: str = None):
        """Usado pelo Worker para salvar"""
        if not task_id or not isinstance(task_id, str):
            raise ValueError("task_id deve ser uma string não vazia")
        if not topic or not isinstance(topic, str):
            raise ValueError("topic deve ser uma string não vazia")
        if not content or not isinstance(content, str):
            raise ValueError("content deve ser uma string não vazia")
        if user_id is not None and (
            not isinstance(user_id, str) or not user_id.strip()
        ):
            raise ValueError("user_id deve ser uma string não vazia ou None")

        redis = get_redis_client()
        key = f"report:{task_id}"

        data = {
            "task_id": task_id,
            "topic": topic,
            "content": content,
            "owner": user_id,
        }

        pipeline = redis.pipeline()
        pipeline.set(key, json.dumps(data))

        if user_id:
            pipeline.sadd(f"user:{user_id}:reports", task_id)

        pipeline.execute()
        logger.info(f"Relatório {task_id} salvo para {user_id}")

    @staticmethod
    def get_by_id(task_id: str, user_id: str = None):
        """Usado pela API para mostrar detalhes"""
        if not task_id or not isinstance(task_id, str):
            raise ValueError("task_id deve ser uma string não vazia")
        if user_id is not None and (
            not isinstance(user_id, str) or not user_id.strip()
        ):
            raise ValueError("user_id deve ser uma string não vazia ou None")

        redis = get_redis_client()
        data = redis.get(f"report:{task_id}")

        if not data:
            raise ValueError("Relatório não encontrado")

        report = json.loads(data)

        if user_id and report.get("owner") != user_id:
            logger.warning(
                f"Acesso negado: User {user_id} tentou ler report de {report.get('owner')}"
            )
            raise ValueError("Acesso negado ao relatório")

        return report

    @staticmethod
    def list_by_user(user_id: str):
        """Usado pela API para listar"""
        if not user_id or not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id deve ser uma string não vazia")

        redis = get_redis_client()
        report_ids = redis.smembers(f"user:{user_id}:reports")
        return list(report_ids)
