"""Serviço central para autenticação e gestão de usuários no Redis."""

import uuid
from utils.redis_client import get_redis_client
from utils.logging import get_logger

logger = get_logger("auth_service")


class AuthService:
    @staticmethod
    def create_user(username: str, token: str = None):
        redis = get_redis_client()
        if not token:
            token = str(uuid.uuid4())

        token_key = f"auth:token:{token}"
        user_key = f"auth:user:{username}"

        if redis.exists(user_key):
            raise ValueError("Usuário já existe")

        pipe = redis.pipeline()
        pipe.set(token_key, username)
        pipe.set(user_key, token)
        pipe.sadd("auth:users_list", username)
        pipe.execute()

        logger.info(f"Usuário criado: {username}")
        return {"username": username, "token": token, "status": "created"}

    @staticmethod
    def list_users():
        redis = get_redis_client()
        return list(redis.smembers("auth:users_list"))

    @staticmethod
    def revoke_user(username: str):
        redis = get_redis_client()
        user_key = f"auth:user:{username}"
        token = redis.get(user_key)

        if not token:
            raise ValueError("Usuário não encontrado")

        pipe = redis.pipeline()
        pipe.delete(f"auth:token:{token}")
        pipe.delete(user_key)
        pipe.srem("auth:users_list", username)
        # TODO: Derrubar sessões ativas poderia ser feito aqui se rastreado
        pipe.execute()

        return {"status": "revoked", "username": username}

    @staticmethod
    def authenticate_by_token(token: str):
        """Verifica se o token existe e retorna o username."""
        redis = get_redis_client()
        username = redis.get(f"auth:token:{token}")
        if not username:
            raise ValueError("Token inválido")
        return username

    @staticmethod
    def create_session(username: str):
        """Gera um ID de sessão e salva no Redis."""
        redis = get_redis_client()
        session_id = str(uuid.uuid4())

        redis.set(f"session:{session_id}", username, ex=86400)
        return session_id

    @staticmethod
    def get_user_by_session(session_id: str):
        """Valida a sessão e retorna o usuário."""
        redis = get_redis_client()
        username = redis.get(f"session:{session_id}")
        return username

    @staticmethod
    def delete_session(session_id: str):
        """Remove a sessão do Redis."""
        if session_id:
            redis = get_redis_client()
            redis.delete(f"session:{session_id}")
