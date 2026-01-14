"""Utilitários de segurança para JWT."""

from datetime import datetime, timedelta, timezone
from jose import jwt
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
    current_time = datetime.now(timezone.utc)
    expire = current_time + timedelta(
        minutes=settings.security_access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    to_encode.update({"nbf": current_time})
    to_encode.update({"iat": current_time})
    to_encode.update({"iss": "NewsGrid-Backend"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.security_api_secret_key,
        algorithm=settings.security_algorithm,
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
            settings.security_api_secret_key,
            algorithms=[settings.security_algorithm],
        )
        return payload.get("sub") or ""
    except Exception:
        return ""
