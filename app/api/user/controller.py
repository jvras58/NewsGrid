"""Controller de Gestão de Usuários."""

import bcrypt
from fastapi import HTTPException

from app.core.database import async_session
from app.services.auth_service_sql import AuthServiceSQL
from utils.logging import get_logger

logger = get_logger("users_controller")


async def create_user_logic(username: str, email: str, password: str):
    try:
        # TODO: Acredito que não faz necessario passar async with async_session() as session podendo colocar direto na chamada da rota com session: AsyncSession = Depends(get_db)
        async with async_session() as session:
            hashed_password = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()
            ).decode()
            await AuthServiceSQL.create_user(session, username, email, hashed_password)
        return {"username": username, "email": email, "status": "created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Erro crítico: {e}")
        raise HTTPException(status_code=500, detail="Erro interno") from e


async def list_users_logic():
    try:
        # TODO: Acredito que não faz necessario passar async with async_session() as session podendo colocar direto na chamada da rota com session: AsyncSession = Depends(get_db)
        async with async_session() as session:
            return await AuthServiceSQL.list_usernames(session)
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=500, detail="Erro interno") from e
