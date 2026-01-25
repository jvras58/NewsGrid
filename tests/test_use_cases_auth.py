from unittest.mock import AsyncMock, patch

import pytest

from app.domain.auth.use_cases import GetCurrentUserUseCase, LoginUseCase


@pytest.mark.asyncio
async def test_login_use_case_success(mock_redis):
    repo = AsyncMock()
    repo.get_by_username.return_value = AsyncMock(
        hashed_password="hashed", username="admin"
    )
    use_case = LoginUseCase(repo)
    with patch("app.domain.auth.use_cases.verify_password", return_value=True):
        token = await use_case.execute(None, "admin", "admin123")
    assert token is not None


@pytest.mark.asyncio
async def test_get_current_user_use_case_success(mock_redis):
    auth_repo = AsyncMock()
    user_repo = AsyncMock()
    auth_repo.get_by_username.return_value = AsyncMock(username="admin")
    user_repo.get_by_username.return_value = AsyncMock(username="admin")
    use_case = GetCurrentUserUseCase(auth_repo, user_repo)
    user = await use_case.execute(None, "admin")
    assert user.username == "admin"
