from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.report_service_sql import ReportServiceSQL
from app.services.task_status_service import task_status_service

from .schemas import TaskStatusResponse

router = APIRouter()


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str, session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Obtém o status de uma tarefa.

    - **task_id**: ID único da tarefa
    - Retorna status e timestamp opcional se disponível
    - Erro 404 se tarefa não encontrada ou expirada
    """
    status = task_status_service.get_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found or expired")

    report = await ReportServiceSQL.get_report_by_task_id(session, task_id)
    created_at = report.created_at if report else None

    return TaskStatusResponse(task_id=task_id, status=status, created_at=created_at)
