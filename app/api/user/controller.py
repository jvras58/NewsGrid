"""Controller de Gestão de Usuários."""

import asyncio

import bcrypt
from fastapi import HTTPException

from app.core.database import async_session
from app.services.auth_service_sql import AuthServiceSQL
from utils.logging import get_logger

logger = get_logger("users_controller")


def create_user_logic(username: str, email: str, password: str):
    async def create():
        async with async_session() as session:
            hashed_password = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()
            ).decode()
            return await AuthServiceSQL.create_user(
                session, username, email, hashed_password
            )

    try:
        asyncio.run(create())
        return {"username": username, "email": email, "status": "created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Erro crítico: {e}")
        raise HTTPException(status_code=500, detail="Erro interno") from e


def list_users_logic():
    async def list_all():
        async with async_session() as session:
            return await AuthServiceSQL.list_usernames(session)

    try:
        return asyncio.run(list_all())
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=500, detail="Erro interno") from e
