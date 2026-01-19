from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.report.entities import ReportEntity
from app.domain.report.repositories import IReportRepository
from app.models.reports import Report as ReportModel


class SQLReportRepository(IReportRepository):
    def _to_entity(self, model: ReportModel) -> ReportEntity:
        return ReportEntity(
            id=model.id,
            task_id=model.task_id,
            owner_id=model.owner_id,
            topic=model.topic,
            content=model.content,
            created_at=model.created_at,
        )

    async def create_report(
        self,
        session: AsyncSession,
        task_id: str,
        owner_id: int,
        topic: str,
        content: str | None,
    ) -> ReportEntity:
        report = ReportModel(
            task_id=task_id, owner_id=owner_id, topic=topic, content=content
        )
        session.add(report)
        try:
            await session.commit()
            await session.refresh(report)
            return self._to_entity(report)
        except Exception as e:
            await session.rollback()
            raise ValueError(f"Erro ao criar relatório: {e}") from e

    async def get_report_by_task_id(
        self, session: AsyncSession, task_id: str
    ) -> ReportEntity | None:
        result = await session.execute(
            select(ReportModel)
            .options(joinedload(ReportModel.owner))
            .where(ReportModel.task_id == task_id)
        )
        model = result.unique().scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_reports_by_owner(
        self,
        session: AsyncSession,
        owner_id: int,
        topic_filter: str | None,
        page: int,
        per_page: int,
    ) -> tuple[list[ReportEntity], int]:
        stmt = select(ReportModel).where(ReportModel.owner_id == owner_id)
        if topic_filter:
            stmt = stmt.where(ReportModel.topic.ilike(f"%{topic_filter}%"))
        stmt = stmt.order_by(ReportModel.created_at.desc())

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await session.execute(count_stmt)
        total = total_result.scalar()

        offset = (page - 1) * per_page
        stmt = (
            stmt.offset(offset).limit(per_page).options(joinedload(ReportModel.owner))
        )

        result = await session.execute(stmt)
        models = result.unique().scalars().all()
        return [self._to_entity(model) for model in models], total
