from dependency_injector import containers, providers

from app2.core.database import get_db
from app2.domain.auth.use_cases import GetCurrentUserUseCase, LoginUseCase
from app2.domain.report.use_cases import (
    GetReportUseCase,
    ListMyReportsUseCase,
    ProcessAnalysisUseCase,
    ProcessResearchUseCase,
    RequestAnalysisUseCase,
)
from app2.domain.status.use_cases import GetTaskStatusUseCase
from app2.domain.user.use_cases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    ListUsersUseCase,
)
from app2.infrastructure.repositories.redis.cache_repository import RedisCacheRepository
from app2.infrastructure.repositories.redis.status_repository import (
    RedisTaskStatusRepository,
)
from app2.infrastructure.repositories.sql.auth_repository import SQLAuthRepository
from app2.infrastructure.repositories.sql.report_repository import SQLReportRepository
from app2.infrastructure.repositories.sql.user_repository import SQLUserRepository


class Container(containers.DeclarativeContainer):
    db_session = providers.Resource(get_db)

    # Repositórios

    auth_repo = providers.Factory(SQLAuthRepository, session=db_session)
    user_repo = providers.Factory(SQLUserRepository, session=db_session)

    task_status_repo = providers.Singleton(RedisTaskStatusRepository)
    cache_repo = providers.Singleton(RedisCacheRepository)
    report_repo = providers.Factory(SQLReportRepository, session=db_session)

    # Use Cases de Auth (usam auth_repo e, se necessário, user_repo)
    login_use_case = providers.Factory(LoginUseCase, auth_repo=auth_repo)
    get_current_user_use_case = providers.Factory(
        GetCurrentUserUseCase, auth_repo=auth_repo, user_repo=user_repo
    )

    # Use Cases de User (usam user_repo)
    create_user_use_case = providers.Factory(CreateUserUseCase, user_repo=user_repo)
    list_users_use_case = providers.Factory(ListUsersUseCase, user_repo=user_repo)
    get_user_by_id_use_case = providers.Factory(GetUserByIdUseCase, user_repo=user_repo)

    # Use Cases de Status
    get_task_status_use_case = providers.Factory(
        GetTaskStatusUseCase, task_status_repo=task_status_repo, report_repo=report_repo
    )

    # Use Cases de Report
    request_analysis_use_case = providers.Factory(
        RequestAnalysisUseCase, cache_repo=cache_repo, task_status_repo=task_status_repo
    )
    get_report_use_case = providers.Factory(GetReportUseCase, report_repo=report_repo)
    list_my_reports_use_case = providers.Factory(
        ListMyReportsUseCase, report_repo=report_repo
    )

    # Use Cases de Processamento
    process_research_use_case = providers.Factory(
        ProcessResearchUseCase, task_status_repo=task_status_repo
    )
    process_analysis_use_case = providers.Factory(
        ProcessAnalysisUseCase,
        report_repo=report_repo,
        cache_repo=cache_repo,
        task_status_repo=task_status_repo,
    )
