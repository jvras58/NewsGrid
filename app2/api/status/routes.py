from fastapi import APIRouter

from app2.api.status.controller import get_task_status_logic
from app2.api.status.schemas import TaskStatusResponse

router = APIRouter()


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Obtém o status de uma tarefa.

    - **task_id**: ID único da tarefa
    - Retorna status e timestamp opcional se disponível
    - Erro 404 se tarefa não encontrada ou expirada
    """
    return await get_task_status_logic(task_id)
