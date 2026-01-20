from sqlalchemy import select

from app.models.user import User
from tests.factory.user_factory import UserFactory


def test_create_user(session):
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
    session.commit()

    # WHEN ------
    # Quando executa-se uma busca com um fultro que aponta para o usuário anteriormente
    # salvo;
    user = session.scalar(select(User).where(User.username == "user.test"))

    # THEN ------
    # Então uma instancia de User é retornada do banco de dados com os mesmos dados que
    # foi salvo anteriormente.
    assert user.username == "user.test"
    assert user.email == new_user.email
    assert user.hashed_password == new_user.hashed_password
    assert user.created_at == new_user.created_at


def test_create_user_success(client):
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "test",
            "email": "testuser@test.com",
            "password": "Qwert123",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["username"] == "test"
    assert response.json()["email"] == "testuser@test.com"
    assert "password" not in response.json()


def test_create_user_already_exists_fail(client, user):
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "Teste",
            "email": "teste@test.com",
            "password": "Qwert123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already exists."
