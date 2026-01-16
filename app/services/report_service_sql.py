from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Report
from utils.exceptions import ReportCreationError
from utils.logging import get_logger

logger = get_logger("report_service_sql")


class ReportServiceSQL:
    """
    Serviço SQL para operações com relatórios.

    Esta classe pode ser usada de duas formas:
    1. Métodos estáticos (compatibilidade): ReportServiceSQL.create_report(session, ...)
    2. Instância com sessão injetada: service = ReportServiceSQL(session); service.create(...)
    """

    def __init__(self, session: AsyncSession | None = None):
        """
        Inicializa o serviço com uma sessão opcional.

        Args:
            session: Sessão async do SQLAlchemy (opcional para uso com métodos estáticos).
        """
        self._session = session

    # =========================================================================
    # Métodos de Instância (Repository Pattern)
    # =========================================================================

    async def create(
        self,
        task_id: str,
        user_id: int,
        topic: str,
        content: str | None = None,
    ) -> dict:
        """
        Cria um novo relatório (método de instância).

        Args:
            task_id: ID único da tarefa.
            user_id: ID do usuário owner.
            topic: Tópico.
            content: Conteúdo (opcional).

        Returns:
            dict: {'status': 'created', 'report_id': int}

        Raises:
            ReportCreationError: Se falhar ao criar.
        """
        if self._session is None:
            raise ValueError(
                "Sessão não configurada. Use o construtor ou métodos estáticos."
            )
        return await self.create_report(self._session, task_id, user_id, topic, content)

    async def get_by_task_id(self, task_id: str) -> Report | None:
        """
        Busca relatório por task_id (método de instância).

        Args:
            task_id: ID da tarefa.

        Returns:
            Report ou None.
        """
        if self._session is None:
            raise ValueError(
                "Sessão não configurada. Use o construtor ou métodos estáticos."
            )
        return await self.get_report_by_task_id(self._session, task_id)

    async def list_by_user(
        self,
        user_id: int,
        topic_filter: str | None = None,
        page: int = 1,
        per_page: int = 10,
    ) -> tuple[list[Report], int]:
        """
        Lista relatórios de um usuário (método de instância).

        Args:
            user_id: ID do usuário.
            topic_filter: Filtro por tópico.
            page: Página.
            per_page: Itens por página.

        Returns:
            (list[Report], total_count)
        """
        if self._session is None:
            raise ValueError(
                "Sessão não configurada. Use o construtor ou métodos estáticos."
            )
        return await self.list_reports(
            self._session, user_id, topic_filter, page, per_page
        )

    # =========================================================================
    # Métodos Estáticos (Compatibilidade)
    # =========================================================================

    @staticmethod
    async def create_report(
        session: AsyncSession,
        task_id: str,
        user_id: int,
        topic: str,
        content: str = None,
    ) -> dict:
        """
        Cria um novo relatório no banco.

        Args:
            session: Sessão async.
            task_id: ID único da tarefa.
            user_id: ID do usuário owner.
            topic: Tópico.
            content: Conteúdo (opcional).

        Returns:
            dict: {'status': 'created', 'report_id': int}

        Raises:
            ReportCreationError: Se falhar ao criar o relatório.
        """
        report = Report(task_id=task_id, owner_id=user_id, topic=topic, content=content)
        session.add(report)
        try:
            await session.commit()
            await session.refresh(report)
            logger.info(f"Relatório criado: {task_id}")
            return {"status": "created", "report_id": report.id}
        except Exception as e:
            await session.rollback()
            raise ReportCreationError(task_id=task_id, reason=str(e)) from e

    @staticmethod
    async def get_report_by_task_id(
        session: AsyncSession, task_id: str
    ) -> Report | None:
        """
        Busca relatório por task_id, com owner eager loaded.

        Args:
            session: Sessão async.
            task_id: ID da tarefa.

        Returns:
            Report ou None.
        """
        result = await session.execute(
            select(Report)
            .options(joinedload(Report.owner))
            .where(Report.task_id == task_id)
        )
        return result.unique().scalar_one_or_none()

    @staticmethod
    async def list_reports(
        session: AsyncSession,
        user_id: int,
        topic_filter: str = None,
        page: int = 1,
        per_page: int = 10,
    ) -> tuple[list[Report], int]:
        """
        Lista relatórios de um usuário, com filtros e paginação.

        Args:
            session: Sessão async.
            user_id: ID do usuário.
            topic_filter: Filtro por tópico (ilike).
            page: Página (1-based).
            per_page: Itens por página.

        Returns:
            (list[Report], total_count)
        """
        stmt = select(Report).where(Report.owner_id == user_id)
        if topic_filter:
            stmt = stmt.where(Report.topic.ilike(f"%{topic_filter}%"))
        stmt = stmt.order_by(Report.created_at.desc())

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await session.execute(count_stmt)
        total = total_result.scalar()

        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page).options(joinedload(Report.owner))

        result = await session.execute(stmt)
        reports = result.unique().scalars().all()

        return reports, total
