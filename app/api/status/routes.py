from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.status.controller import get_task_status_logic
from app.api.status.schemas import TaskStatusResponse
from app.core.database import get_db

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_db)]


@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str, session: Session):
    """
    Obtém o status de uma tarefa.

    - **task_id**: ID único da tarefa
    - Retorna status e timestamp opcional se disponível
    - Erro 404 se tarefa não encontrada ou expirada
    """
    return await get_task_status_logic(task_id, session)
