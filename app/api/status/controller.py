from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.status.schemas import TaskStatusResponse
from app.core.container import Container

container = Container()


async def get_task_status_logic(
    task_id: str, session: AsyncSession
) -> TaskStatusResponse:
    use_case = container.get_task_status_use_case()
    try:
        entity = await use_case.execute(session, task_id)
        return TaskStatusResponse.from_entity(entity)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
