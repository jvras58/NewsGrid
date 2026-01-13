"""
Lógica de rotas para análise de tópicos.
"""

from fastapi import APIRouter, Query, HTTPException, Path, Depends
from .controller import request_analysis_logic
from app.services.report_service import ReportService
from app.api.auth.controller import verify_session
from utils.logging import get_logger

logger = get_logger(__name__)

# TODO: Retirar a dependência global para ficar somente nas rotas mesmo!
router = APIRouter(dependencies=[Depends(verify_session)])


@router.post("/")
async def request_analysis(
    topic: str = Query(..., description="Tópico para análise"),
    username: str = Depends(verify_session),
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
    username: str = Depends(verify_session),
):
    try:
        report = ReportService.get_by_id(task_id, user_id=username)
        return report
    except ValueError as e:
        logger.warning(f"Erro ao buscar relatório: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/my-reports")
async def list_my_reports(username: str = Depends(verify_session)):
    try:
        ids = ReportService.list_by_user(username)
        return {"user": username, "reports": ids}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
