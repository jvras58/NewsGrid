from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth.controller import get_current_user
from app.api.report.controller import (
    get_report_logic,
    list_my_reports_logic,
    request_analysis_logic,
)
from app.api.report.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    MyReportsResponse,
    ReportResponse,
)
from app.domain.user.entities import UserEntity

router = APIRouter()

get_current_user_dep = Annotated[UserEntity, Depends(get_current_user)]


@router.post("/", response_model=AnalyzeResponse)
async def request_analysis(request: AnalyzeRequest, current_user: get_current_user_dep):
    return request_analysis_logic(request, current_user.id)


@router.get("/report/{task_id}", response_model=ReportResponse)
async def get_analysis_report(task_id: str, current_user: get_current_user_dep):
    return await get_report_logic(task_id, current_user.id)


@router.get("/my-reports", response_model=MyReportsResponse)
async def list_my_reports(current_user: get_current_user_dep):
    return await list_my_reports_logic(current_user.id)
