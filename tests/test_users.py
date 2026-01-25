from unittest.mock import patch

import pytest
from sqlalchemy import select

from app.models.user import User
from tests.factory.user_factory import UserFactory


@pytest.mark.asyncio
async def test_create_user(session):
    """
    Teste de criação de User no banco de dados.

    Args:
        session (Session): Instancia de Session do SQLAlchemy provisionada pelo Fixture.
    """

    # GIVEN ------
    # Dada uma Instancia de User com os dados abaixo é salva no banco de dados;
    new_user = UserFactory.build()
    new_user.id = None
    new_user.username = "user.test"
    session.add(new_user)
    await session.commit()

    # WHEN ------
    # Quando executa-se uma busca com um filtro que aponta para o usuário anteriormente
    # salvo;
    user = await session.scalar(select(User).where(User.username == "user.test"))

    # THEN ------
    # Então uma instancia de User é retornada do banco de dados com os mesmos dados que
    # foi salvo anteriormente.
    assert user.username == "user.test"
    assert user.email == new_user.email
    assert user.hashed_password == new_user.hashed_password
    assert user.created_at == new_user.created_at


@pytest.mark.asyncio
async def test_create_user_success(container, session):
    use_case = container.create_user_use_case()
    with patch.object(use_case, "execute", return_value=None) as mock_execute:
        await use_case.execute(session, "test", "testuser@test.com", "Qwert123")
        mock_execute.assert_called_once_with(
            session, "test", "testuser@test.com", "Qwert123"
        )


@pytest.mark.asyncio
async def test_list_users_success(container, user, session):
    use_case = container.list_users_use_case()
    with patch.object(use_case, "execute", return_value=[user]) as mock_execute:
        result = await use_case.execute(session, user.username, 1, 10)
        assert len(result) == 1
        mock_execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_success(container, user, session):
    use_case = container.get_user_by_id_use_case()
    with patch.object(use_case, "execute", return_value=user) as mock_execute:
        result = await use_case.execute(session, user.id)
        assert result.username == user.username
        mock_execute.assert_called_once_with(session, user.id)
