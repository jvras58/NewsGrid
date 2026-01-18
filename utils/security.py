"""Utilitários de segurança para JWT."""

import logging
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from jwt import PyJWTError

from utils.settings import settings


def create_access_token(data: dict) -> str:
    """
    Cria um token JWT de acesso.

    Args:
        data: Dicionário com os dados a serem codificados no token.
              Deve conter 'sub' com o username.

    Returns:
        str: Token JWT codificado.
    """
    to_encode = data.copy()
    current_time = datetime.now(UTC)
    expire = current_time + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    to_encode.update({"nbf": current_time})
    to_encode.update({"iat": current_time})
    to_encode.update({"iss": "NewsGrid-Backend"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def extract_username(jwt_token: str) -> str:
    """
    Extrai o username do payload do token JWT.

    Args:
        jwt_token: Token JWT a ser decodificado.

    Returns:
        str: Username extraído do token, ou string vazia se inválido.
    """
    try:
        payload = jwt.decode(
            jwt_token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload.get("sub") or ""
    except PyJWTError as e:
        logging.error(f"JWT decoding error: {e}")
        return ""


def hash_password(password: str) -> str:
    """
    Hashea a senha usando bcrypt.

    Args:
        password: Senha em plain text.

    Returns:
        str: Hash da senha.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    Verifica se a senha plain corresponde ao hash.

    Args:
        hashed_password: Hash da senha.
        plain_password: Senha em plain text.

    Returns:
        bool: True se corresponde.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
