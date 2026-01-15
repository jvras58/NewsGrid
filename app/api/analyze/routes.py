"""
Lógica de rotas para análise de tópicos.
"""

from fastapi import APIRouter, Depends

from app.api.auth.controller import get_current_user
from utils.logging import get_logger

from .controller import request_analysis_logic
from .schemas import AnalyzeRequest, AnalyzeResponse

logger = get_logger(__name__)
router = APIRouter()

# TODO: Habilitar rate limiting (Configurar adequadamente)
# rate_limit_dep = get_rate_limit_dependency()


@router.post("/", response_model=AnalyzeResponse)
async def request_analysis(
    request: AnalyzeRequest,
    user_id: int = Depends(get_current_user),
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
    result = request_analysis_logic(request.topic, user_id)
    logger.info(
        f"Resposta enviada para tópico {request.topic}: {result.get('status', 'unknown')}"
    )
    return AnalyzeResponse(**result)
