from dataclasses import dataclass


@dataclass
class AuthEntity:
    """Entidade de domínio pura para Autenticação (focada em credenciais)."""

    id: int | None
    username: str
    hashed_password: str
