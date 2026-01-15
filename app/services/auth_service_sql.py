import bcrypt
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from utils.exceptions import (
    BadRequestError,
    UserAlreadyExistsError,
)
from utils.logging import get_logger

logger = get_logger("auth_service_sql")


class AuthServiceSQL:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashea a senha usando bcrypt.

        Args:
            password: Senha em plain text.

        Returns:
            str: Hash da senha.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    async def create_user(
        session: AsyncSession, username: str, email: str, password: str
    ) -> dict:
        """
        Cria um novo usuário no banco de dados.

        Args:
            session: Sessão assíncrona do SQLAlchemy.
            username: Nome de usuário único.
            email: Email único.
            password: Senha em plain text.

        Returns:
            dict: {'status': 'created', 'user_id': int}

        Raises:
            BadRequestError: Se username, email ou password estiverem vazios.
            UserAlreadyExistsError: Se username ou email já existir.
        """
        if not username or not email or not password:
            raise BadRequestError("Username, email e password são obrigatórios")

        hashed_password = AuthServiceSQL.hash_password(password)
        user = User(username=username, email=email, hashed_password=hashed_password)
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
            logger.info(f"Usuário criado: {username}")
            return {"status": "created", "user_id": user.id}
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()
            if "username" in error_msg:
                raise UserAlreadyExistsError("Username já existe") from e
            elif "email" in error_msg:
                raise UserAlreadyExistsError("Email já existe") from e
            raise BadRequestError("Erro ao criar usuário") from e

    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
        """
        Busca usuário por username.

        Args:
            session: Sessão assíncrona.
            username: Nome de usuário.

        Returns:
            User ou None.
        """
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
        """
        Busca usuário por email.

        Args:
            session: Sessão assíncrona.
            email: Email.

        Returns:
            User ou None.
        """
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_usernames(session: AsyncSession) -> list[str]:
        """
        Lista usernames de usuários.

        Args:
            session: Sessão async.

        Returns:
            list[str]: Lista de usernames.
        """
        stmt = select(User.username)
        result = await session.execute(stmt)
        return result.scalars().all()
