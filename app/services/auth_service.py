"""Serviço central para autenticação e gestão de usuários no Redis."""

import uuid
from redis.exceptions import WatchError
from utils.redis_client import get_redis_client
from utils.logging import get_logger

logger = get_logger("auth_service")


class AuthService:
    @staticmethod
    def create_user(username: str, token: str = None):
        """
        Cria um novo usuário no Redis com o nome de usuário fornecido e um token opcional.

        Este método gera um token UUID se não for fornecido, e armazena as associações no Redis de forma atômica
        usando pipeline e watch para evitar conflitos em caso de criação simultânea.

        Args:
            username (str): O nome do usuário a ser criado. Deve ser único.
            token (str, optional): O token de autenticação. Se não fornecido, um UUID é gerado automaticamente.

        Returns:
            dict: Um dicionário contendo 'username', 'token' e 'status' indicando que o usuário foi criado.

        Raises:
            ValueError: Se o usuário já existir ou se houver falha após múltiplas tentativas devido a contenção alta no Redis.
        """
        redis = get_redis_client()
        if not token:
            token = str(uuid.uuid4())

        token_key = f"auth:token:{token}"
        user_key = f"auth:user:{username}"

        max_retries = 5
        with redis.pipeline() as pipe:
            for attempt in range(max_retries):
                try:
                    pipe.watch(user_key)
                    if pipe.exists(user_key):
                        pipe.unwatch()
                        raise ValueError("Usuário já existe")
                    pipe.multi()
                    pipe.set(token_key, username)
                    pipe.set(user_key, token)
                    pipe.sadd("auth:users_list", username)
                    pipe.execute()
                    break
                except WatchError:
                    if attempt == max_retries - 1:
                        raise ValueError(
                            "Falha ao criar usuário devido a contenção alta no Redis após múltiplas tentativas"
                        )
                    continue

        logger.info(f"Usuário criado: {username}")
        return {"username": username, "token": token, "status": "created"}

    @staticmethod
    def list_users():
        """
        Lista todos os usuários registrados no sistema.

        Este método recupera o conjunto de nomes de usuários armazenados no Redis.

        Returns:
            list: Uma lista de strings representando os nomes dos usuários registrados.
        """
        redis = get_redis_client()
        users = redis.smembers("auth:users_list")
        return [u.decode("utf-8") if isinstance(u, bytes) else u for u in users]

    @staticmethod
    def revoke_user(username: str):
        """
        Revoga um usuário, removendo seu token, chave de usuário e todas as sessões associadas.

        Este método deleta as chaves relacionadas ao usuário no Redis, incluindo token, dados do usuário,
        remoção da lista de usuários e limpeza de sessões ativas.

        Args:
            username (str): O nome do usuário a ser revogado.

        Returns:
            dict: Um dicionário contendo 'status' ('revoked') e 'username'.

        Raises:
            ValueError: Se o usuário não for encontrado.
        """
        redis = get_redis_client()
        user_key = f"auth:user:{username}"
        token = redis.get(user_key)

        if not token:
            raise ValueError("Usuário não encontrado")

        if isinstance(token, bytes):
            token = token.decode("utf-8")

        pipe = redis.pipeline()
        pipe.delete(f"auth:token:{token}")
        pipe.delete(user_key)
        pipe.srem("auth:users_list", username)
        pipe.execute()

        return {"status": "revoked", "username": username}

    @staticmethod
    def user_exists(username: str):
        """
        Verifica se um usuário existe no sistema.

        Args:
            username (str): O nome do usuário a ser verificado.

        Returns:
            bool: True se o usuário existir, False caso contrário.
        """
        redis = get_redis_client()
        return bool(redis.exists(f"auth:user:{username}"))

    @staticmethod
    def authenticate_by_token(token: str):
        """
        Autentica um usuário pelo token fornecido, verificando sua validade e existência.

        Este método valida o formato do token como UUID e busca o nome de usuário associado no Redis.

        Args:
            token (str): O token de autenticação a ser verificado.

        Returns:
            str: O nome do usuário associado ao token.

        Raises:
            ValueError: Se o token for inválido (formato incorreto ou não existir no Redis).
        """
        if not token or not isinstance(token, str):
            raise ValueError("Token inválido")
        try:
            uuid.UUID(token)
        except ValueError:
            raise ValueError("Token inválido")
        redis = get_redis_client()
        username = redis.get(f"auth:token:{token}")
        if not username:
            raise ValueError("Token inválido")
        if isinstance(username, bytes):
            username = username.decode("utf-8")
        return username
