"""
Lógica de rotas para análise de tópicos.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.controller import get_current_user
from app.core.database import get_db
from app.models import User
from utils.logging import get_logger

from .controller import get_report_logic, list_my_reports_logic, request_analysis_logic
from .schemas import AnalyzeRequest, AnalyzeResponse, MyReportsResponse, ReportResponse

logger = get_logger(__name__)
router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_db)]
get_current_user_dep = Annotated[User, Depends(get_current_user)]

# TODO: Habilitar rate limiting (Configurar adequadamente)
# rate_limit_dep = get_rate_limit_dependency()


@router.post("/", response_model=AnalyzeResponse)
async def request_analysis(
    request: AnalyzeRequest,
    current_user: get_current_user_dep,
    # _rate_limited: bool = Depends(rate_limit_dep),
):
    """
    Inicia análise de tópico.

    - Autentica usuário via Postgres.
    - Checa cache Redis.
    - Se não cached, gera task_id, seta status e enfileira no RabbitMQ.
    - Retorna task_id imediatamente.
    """
    logger.info(f"Requisição recebida para análise de tópico: {request.topic}")
    result = request_analysis_logic(request.topic, current_user.id)
    logger.info(
        f"Resposta enviada para tópico {request.topic}: {result.get('status', 'unknown')}"
    )
    return AnalyzeResponse(**result)


@router.get("/report/{task_id}", response_model=ReportResponse)
async def get_analysis_report(
    task_id: str,
    current_user: get_current_user_dep,
    db=Session,
):
    """
    Obtém relatório por task_id.

    - Autentica usuário.
    - Retorna relatório se pertencer ao usuário.
    """
    try:
        report = await get_report_logic(task_id, current_user.id, db)
        return report
    except ValueError as e:
        raise HTTPException(
            status_code=404 if "não encontrado" in str(e) else 403, detail=str(e)
        ) from e


@router.get("/my-reports", response_model=MyReportsResponse)
async def list_my_reports(
    current_user: get_current_user_dep,
    db=Session,
):
    """
    Lista relatórios do usuário.

    - Autentica usuário.
    - Retorna lista de task_ids.
    """
    try:
        result = await list_my_reports_logic(current_user.id, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
