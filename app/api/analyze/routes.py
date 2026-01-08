"""
Lógica de rotas para análise de tópicos.
"""

from fastapi import APIRouter, Query
from .controller import request_analysis_logic

router = APIRouter()


@router.post("/")
async def request_analysis(topic: str = Query(..., description="Tópico para análise")):
    return request_analysis_logic(topic)
