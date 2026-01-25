import pytest

from app.infrastructure.repositories.sql.user_repository import SQLUserRepository


@pytest.mark.asyncio
async def test_sql_user_repository_get_by_id(session):
    repo = SQLUserRepository()
    user = await repo.get_by_id(session, 1)
    assert user is None
