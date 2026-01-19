from app.domain.rate_limit.entities import RateLimitEntity
from app.domain.rate_limit.repositories import IRateLimitRepository
from utils.exceptions import BadRequestError


class CheckRateLimitUseCase:
    def __init__(self, rate_limit_repo: IRateLimitRepository):
        self.rate_limit_repo = rate_limit_repo

    def execute(self, identifier: str) -> RateLimitEntity:
        limit = self.rate_limit_repo.get_user_limit(identifier)
        allowed, current_count, reset_in = self.rate_limit_repo.check_rate_limit(
            identifier, limit
        )

        entity = RateLimitEntity(
            identifier=identifier,
            limit=limit,
            current_count=current_count,
            reset_in_seconds=reset_in,
            allowed=allowed,
        )
        entity.validate()

        if not allowed:
            raise BadRequestError(
                f"Limite de taxa excedido. Reset em {reset_in} segundos."
            )

        return entity
