"""
Lógica de rotas para análise de tópicos.
"""

from fastapi import APIRouter, Query, HTTPException
from .controller import request_analysis_logic
from utils.reporting import get_report
from utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/")
async def request_analysis(topic: str = Query(..., description="Tópico para análise")):
    logger.info(f"Requisição recebida para análise de tópico: {topic}")
    result = request_analysis_logic(topic)
    logger.info(
        f"Resposta enviada para tópico {topic}: {result.get('status', 'unknown')}"
    )
    return result


@router.get("/report/{task_id}")
async def get_analysis_report(
    task_id: str = Query(..., description="ID da tarefa para recuperar o relatório"),
):
    logger.info(f"Requisição para recuperar relatório de task_id: {task_id}")
    report = get_report(task_id)
    if report:
        logger.info(f"Relatório encontrado para task_id: {task_id}")
        return report
    else:
        logger.warning(f"Relatório não encontrado para task_id: {task_id}")
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
