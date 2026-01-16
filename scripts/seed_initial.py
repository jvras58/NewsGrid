"""Script para popular o Postgres com um usuário inicial padrão."""

import asyncio

from app.core.database import async_session
from app.services.auth_service_sql import AuthServiceSQL
from utils.logging import get_logger
from utils.settings import settings

logger = get_logger("seed_initial")


async def seed_initial_user():
    """
    Cria um usuário padrão no Postgres se não existir.
    """
    async with async_session() as session:
        user = await AuthServiceSQL.get_user_by_username(session, "admin")
        if not user:
            await AuthServiceSQL.create_user(
                session, "admin", "admin@example.com", settings.default_user_password
            )
            logger.info("🔑 Usuário inicial 'admin' criado no Postgres.")
        else:
            logger.info("🔑 Usuário inicial já existe no Postgres.")


def main():
    asyncio.run(seed_initial_user())


if __name__ == "__main__":
    main()
