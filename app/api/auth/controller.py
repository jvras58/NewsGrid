"""Controller para operações de autenticação de usuários."""

import uuid
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from utils.redis_client import get_redis_client
from utils.logging import get_logger

logger = get_logger("auth_controller")

security = HTTPBearer()


def create_user_logic(username: str, token: str = None):
    redis = get_redis_client()

    if not token:
        token = str(uuid.uuid4())

    token_key = f"auth:token:{token}"
    user_key = f"auth:user:{username}"

    if redis.exists(user_key):
        raise HTTPException(status_code=400, detail="Usuário já existe")

    try:
        redis.set(token_key, username)

        redis.set(user_key, token)

        redis.sadd("auth:users_list", username)

        logger.info(f"Novo usuário criado: {username}")
        return {"username": username, "token": token, "status": "created"}

    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao salvar usuário")


def list_users_logic():
    redis = get_redis_client()
    try:
        users = redis.smembers("auth:users_list")
        return list(users)
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        return []


def revoke_user_logic(username: str):
    """Remove o acesso de um usuário"""
    redis = get_redis_client()
    user_key = f"auth:user:{username}"

    token = redis.get(user_key)
    if token:
        redis.delete(f"auth:token:{token}")
        redis.delete(user_key)
        redis.srem("auth:users_list", username)
        return {"status": "revoked", "username": username}

    raise HTTPException(status_code=404, detail="Usuário não encontrado")


def verify_token(credentials=Depends(security)):
    """Verifica o token de autorização e retorna o username."""
    token = credentials.credentials

    redis = get_redis_client()
    username = redis.get(f"auth:token:{token}")

    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")

    return username.decode("utf-8") if isinstance(username, bytes) else username
