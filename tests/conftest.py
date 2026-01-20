from unittest.mock import MagicMock

import pytest
from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.container import Container
from app.models import Base
from app.models.reports import Report
from app.models.user import User
from utils.security import hash_password


@pytest.fixture
async def session():
    """
    Sessão de banco de dados assíncrona para testes, usando SQLite em memória.
    """
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@event.listens_for(create_async_engine, "connect")
def set_sqlite_pragma(dbapi_connection, _connection_record):
    """
    Ativa foreign keys no SQLite.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def mock_redis():
    return MagicMock()


@pytest.fixture
def mock_rabbitmq():
    return MagicMock()


@pytest.fixture
def container(mock_redis, mock_rabbitmq):
    container = Container()
    container.task_status_repo.override(mock_redis)
    container.cache_repo.override(mock_redis)
    container.rate_limit_repo.override(mock_redis)
    container.message_broker.override(mock_rabbitmq)
    return container


@pytest.fixture
async def user(session):
    """
    Fixture para criar um usuário de teste.
    """
    clr_password = "testtest"
    user = User(
        username="Teste",
        email="teste@test.com",
        password=hash_password(clr_password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    user.clear_password = clr_password
    return user


@pytest.fixture
async def report_user(session, user):
    """
    Fixture para criar um report de teste associado ao user.
    """
    report = Report(
        task_id="test_task_123",
        topic="Tema teste",
        content="Conteúdo teste",
        owner_id=user.id,
    )
    session.add(report)
    await session.commit()
    await session.refresh(report)
    return report
