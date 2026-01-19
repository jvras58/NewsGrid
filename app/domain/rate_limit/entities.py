from dataclasses import dataclass


@dataclass
class RateLimitEntity:
    """Entidade de domínio pura para Rate Limiting."""

    identifier: str
    limit: int
    current_count: int
    reset_in_seconds: int
    allowed: bool

    def validate(self):
        """Validações básicas."""
        if self.limit < 0:
            raise ValueError("Limite deve ser positivo")
        if self.current_count < 0:
            raise ValueError("Contagem atual deve ser não-negativa")
