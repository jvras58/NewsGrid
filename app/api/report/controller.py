from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.report.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    MyReportsResponse,
    ReportResponse,
)
from app.core.container import Container

container = Container()


def request_analysis_logic(request: AnalyzeRequest, user_id: int) -> AnalyzeResponse:
    use_case = container.request_analysis_use_case()
    try:
        result = use_case.execute(request.topic, user_id)
        return AnalyzeResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


async def get_report_logic(
    task_id: str, user_id: int, session: AsyncSession
) -> ReportResponse:
    use_case = container.get_report_use_case()
    try:
        entity = await use_case.execute(session, task_id, user_id)
        return ReportResponse.from_entity(entity)
    except Exception as e:
        raise HTTPException(
            status_code=404 if "não encontrado" in str(e) else 403, detail=str(e)
        ) from e


async def list_my_reports_logic(
    user_id: int, session: AsyncSession
) -> MyReportsResponse:
    use_case = container.list_my_reports_use_case()
    try:
        task_ids, _ = await use_case.execute(session, user_id, None, 1, 10)
        return MyReportsResponse(user=user_id, reports=task_ids)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
