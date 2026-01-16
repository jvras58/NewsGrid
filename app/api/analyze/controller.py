"""
Lógica de negócio para requisições de análise.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.report_cache_service import get_cached_report, make_cache_key
from app.services.report_service_sql import ReportServiceSQL
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


async def get_report_logic(task_id: str, user_id: int, db: AsyncSession):
    """
    Lógica para obter relatório por task_id.

    Args:
        task_id (str): ID da tarefa.
        user_id (int): ID do usuário.
        db (AsyncSession): Sessão do banco.

    Returns:
        dict: Relatório ou erro.
    """
    logger.info(f"Obtendo relatório para task_id: {task_id} | User ID: {user_id}")

    try:
        report = await ReportServiceSQL.get_report_by_task_id(db, task_id)
        if not report:
            raise ValueError("Relatório não encontrado")
        if report.owner_id != user_id:
            raise ValueError("Acesso negado ao relatório")
        return {
            "task_id": report.task_id,
            "topic": report.topic,
            "content": report.content,
            "owner": report.owner_id,
        }
    except ValueError as e:
        logger.error(f"Erro ao obter relatório {task_id}: {str(e)}")
        raise


async def list_my_reports_logic(user_id: int, db: AsyncSession):
    """
    Lógica para listar relatórios do usuário.

    Args:
        user_id (int): ID do usuário.
        db (AsyncSession): Sessão do banco.

    Returns:
        dict: Lista de task_ids.
    """
    logger.info(f"Listando relatórios para user_id: {user_id}")

    try:
        reports, _ = await ReportServiceSQL.list_reports(db, user_id)
        task_ids = [report.task_id for report in reports]
        return {"user": user_id, "reports": task_ids}
    except Exception as e:
        logger.error(f"Erro ao listar relatórios para {user_id}: {str(e)}")
        raise
