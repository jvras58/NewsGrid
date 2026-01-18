from pydantic import BaseModel, ConfigDict, Field

from app.domain.report.entities import ReportEntity


class AnalyzeRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Tópico para análise (ex: 'Impacto da IA no mercado').",
        examples=["Inteligência Artificial em 2025"],
    )


class AnalyzeResponse(BaseModel):
    status: str = Field(..., description="Status da operação.")
    task_id: str | None = Field(
        None, description="ID da tarefa gerada (se não cached)."
    )
    report: dict | None = Field(None, description="Relatório cached (se disponível).")
    error: str | None = Field(None, description="Mensagem de erro (se falhou).")

    model_config = ConfigDict(
        json_schema_extra={
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
    )


class ReportResponse(BaseModel):
    task_id: str = Field(..., description="ID da tarefa.")
    topic: str = Field(..., description="Tópico analisado.")
    content: str = Field(..., description="Conteúdo do relatório.")
    owner: int = Field(..., description="ID do proprietário.")

    @classmethod
    def from_entity(cls, entity: ReportEntity) -> "ReportResponse":
        return cls(
            task_id=entity.task_id,
            topic=entity.topic,
            content=entity.content or "",
            owner=entity.owner_id,
        )


class MyReportsResponse(BaseModel):
    user: int = Field(..., description="ID do usuário.")
    reports: list[str] = Field(..., description="Lista de task_ids dos relatórios.")
