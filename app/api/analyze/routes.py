"""
Lógica de rotas para análise de tópicos.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.api.auth.controller import get_current_user

# from app.api.dependencies import get_rate_limit_dependency
from app.services.report_service import ReportService
from utils.logging import get_logger

from .controller import request_analysis_logic

logger = get_logger(__name__)
router = APIRouter()

# TODO: Habilitar rate limiting (Configurar adequadamente)
# rate_limit_dep = get_rate_limit_dependency()


@router.post("/")
async def request_analysis(
    topic: str = Query(..., description="Tópico para análise"),
    username: str = Depends(get_current_user),
    # _rate_limited: bool = Depends(rate_limit_dep),
):
    logger.info(f"Requisição recebida para análise de tópico: {topic}")
    result = request_analysis_logic(topic, username)
    logger.info(
        f"Resposta enviada para tópico {topic}: {result.get('status', 'unknown')}"
    )
    return result


@router.get("/report/{task_id}")
async def get_analysis_report(
    task_id: str = Path(..., description="ID da tarefa para recuperar o relatório"),
    username: str = Depends(get_current_user),
):
    try:
        report = ReportService.get_by_id(task_id, user_id=username)
        return report
    except ValueError as e:
        logger.warning(f"Erro ao buscar relatório: {e}")
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/my-reports")
async def list_my_reports(username: str = Depends(get_current_user)):
    try:
        ids = ReportService.list_by_user(username)
        return {"user": username, "reports": ids}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
