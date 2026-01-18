from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    """Entidade de domínio pura para Usuário."""

    id: int | None
    username: str
    email: str
    hashed_password: str
    created_at: datetime

    def validate(self):
        """Validações básicas de domínio."""
        if not self.username or len(self.username) < 3:
            raise ValueError("Username deve ter pelo menos 3 caracteres")
        if not self.email or "@" not in self.email:
            raise ValueError("Email inválido")
