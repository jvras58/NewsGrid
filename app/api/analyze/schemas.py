"""
Schemas para requisições de análise.
"""

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request para iniciar análise."""

    topic: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Tópico para análise (ex: 'Impacto da IA no mercado').",
        examples=["Inteligência Artificial em 2025"],
    )


class AnalyzeResponse(BaseModel):
    """Response para análise."""

    status: str = Field(..., description="Status da operação.")
    task_id: str | None = Field(
        None, description="ID da tarefa gerada (se não cached)."
    )
    report: dict | None = Field(None, description="Relatório cached (se disponível).")
    error: str | None = Field(None, description="Mensagem de erro (se falhou).")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "status": "Processamento iniciado",
                    "task_id": "123e4567-e89b-12d3-a456-426614174000",
                },
                {
                    "status": "cached",
                    "report": {
                        "task_id": "abc",
                        "topic": "IA",
                        "content": "...",
                        "owner": 1,
                    },
                },
                {"status": "Falha ao iniciar o processamento", "error": "Erro na fila"},
            ]
        }
