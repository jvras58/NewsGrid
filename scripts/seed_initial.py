"""Script para popular o Redis com um usuário inicial padrão."""

from utils.redis_client import get_redis_client
from utils.logging import get_logger
from utils.settings import settings

logger = get_logger("seed_initial")


def seed_initial_user():
    """
    Cria um usuário padrão no Redis se não existir.

    Salva no Redis: Chave "auth:token:{token}" -> Valor "{user}"
                     Chave "auth:user:{user}" -> Valor "{token}"
                     Adiciona à "auth:users_list"
    """
    try:
        redis = get_redis_client()

        default_token = settings.default_token
        user_data = "admin"

        user_key = f"auth:user:{user_data}"

        if not redis.exists(user_key):
            token_key = f"auth:token:{default_token}"
            pipe = redis.pipeline()
            pipe.set(token_key, user_data)
            pipe.set(user_key, default_token)
            pipe.sadd("auth:users_list", user_data)
            pipe.execute()
            logger.info(
                "🔑 Seed de Auth realizado. Usuário padrão configurado no Redis."
            )
        else:
            logger.info("🔑 Usuário padrão já existe no Redis.")
    except Exception as e:
        logger.error(f"Erro durante o seed inicial do usuário: {e}")
        raise


if __name__ == "__main__":
    seed_initial_user()
