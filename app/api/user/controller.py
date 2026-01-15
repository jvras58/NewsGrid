"""Controller de Gestão de Usuários."""

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_service_sql import AuthServiceSQL
from utils.logging import get_logger

logger = get_logger("users_controller")


async def create_user_logic(
    username: str, email: str, password: str, session: AsyncSession
):
    try:
        result = await AuthServiceSQL.create_user(session, username, email, password)
        return {
            "username": username,
            "email": email,
            "status": "created",
            "user_id": result["user_id"],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Erro crítico: {e}")
        raise HTTPException(status_code=500, detail="Erro interno") from e


async def list_users_logic(session: AsyncSession):
    try:
        return await AuthServiceSQL.list_usernames(session)
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=500, detail="Erro interno") from e


async def get_user_logic(user_id: int, session: AsyncSession):
    try:
        user = await AuthServiceSQL.get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        }
    except Exception as e:
        logger.error(f"Erro ao buscar usuário {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno") from e
