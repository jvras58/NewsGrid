"""
Lógica de rotas para análise de tópicos.
"""

from fastapi import APIRouter, Query
from .controller import request_analysis_logic
from utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/")
async def request_analysis(topic: str = Query(..., description="Tópico para análise")):
    logger.info(f"Requisição recebida para análise de tópico: {topic}")
    result = request_analysis_logic(topic)
    logger.info(f"Resposta enviada para tópico {topic}: {result.get('status', 'unknown')}")
    return result
