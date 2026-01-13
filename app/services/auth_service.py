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
            list: Uma lista de bytes representando os nomes dos usuários registrados.
        """
        redis = get_redis_client()
        return list(redis.smembers("auth:users_list"))

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

        pipe = redis.pipeline()
        pipe.delete(f"auth:token:{token}")
        pipe.delete(user_key)
        pipe.srem("auth:users_list", username)
        try:
            session_keys = redis.keys("session:*")
        except Exception as e:
            logger.error(
                f"Erro ao buscar sessões para revogação de usuário {username}: {e}"
            )
            session_keys = []

        for session_key in session_keys:
            try:
                session_username = redis.get(session_key)
            except Exception as e:
                logger.error(
                    f"Erro ao obter sessão {session_key} para revogação de usuário {username}: {e}"
                )
                continue

            if session_username == username:
                pipe.delete(session_key)
            elif isinstance(session_username, bytes):
                try:
                    if session_username.decode("utf-8") == username:
                        pipe.delete(session_key)
                except Exception as e:
                    logger.error(
                        f"Erro ao decodificar valor da sessão {session_key}: {e}"
                    )
                    continue
        pipe.execute()

        return {"status": "revoked", "username": username}

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
        return username

    @staticmethod
    def create_session(username: str):
        """
        Cria uma nova sessão para o usuário fornecido, gerando um ID único e armazenando no Redis.

        A sessão é definida para expirar após 24 horas (86400 segundos).

        Args:
            username (str): O nome do usuário para o qual a sessão será criada.

        Returns:
            str: O ID da sessão gerada.

        Raises:
            ValueError: Se o username for inválido (vazio ou não string).
        """
        if not username or not isinstance(username, str) or username.strip() == "":
            raise ValueError("Username inválido")
        redis = get_redis_client()
        session_id = str(uuid.uuid4())

        redis.set(f"session:{session_id}", username, ex=86400)
        return session_id

    @staticmethod
    def get_user_by_session(session_id: str):
        """
        Recupera o nome do usuário associado ao ID de sessão fornecido, validando a sessão.

        Este método verifica se a sessão existe no Redis e retorna o usuário correspondente.

        Args:
            session_id (str): O ID da sessão a ser validada.

        Returns:
            str or None: O nome do usuário se a sessão for válida e existir, caso contrário None.

        Raises:
            ValueError: Se o session_id for inválido (formato incorreto).
        """
        if not session_id or not isinstance(session_id, str):
            raise ValueError("Session ID inválido")
        try:
            uuid.UUID(session_id)
        except ValueError:
            raise ValueError("Session ID inválido")
        redis = get_redis_client()
        username = redis.get(f"session:{session_id}")
        if username and isinstance(username, bytes):
            username = username.decode("utf-8")
        return username

    @staticmethod
    def delete_session(session_id: str):
        """
        Remove a sessão do Redis pelo ID fornecido.

        Este método deleta a chave da sessão no Redis, efetivamente encerrando a sessão.

        Args:
            session_id (str): O ID da sessão a ser removida. Se None ou vazio, nenhuma ação é tomada.
        """
        if session_id:
            redis = get_redis_client()
            redis.delete(f"session:{session_id}")
