"""
Serviço para rate limiting usando Redis com sliding window.
"""

import time

from app.domain.rate_limit.repositories import IRateLimitRepository
from app.infrastructure.cache.redis_client import get_redis_client

WINDOW_SECONDS = 60


class RedisRateLimitRepository(IRateLimitRepository):
    def check_rate_limit(self, identifier: str, limit: int) -> tuple[bool, int, int]:
        client = get_redis_client()
        key = f"rate_limit:{identifier}"
        now = time.time()
        window_start = now - WINDOW_SECONDS

        client.zadd(key, {str(now): now})
        client.zremrangebyscore(key, "-inf", window_start)
        count = client.zcard(key)
        client.expire(key, WINDOW_SECONDS)

        allowed = count <= limit
        reset_in = int(WINDOW_SECONDS - (now - window_start))
        return allowed, count, reset_in

    def get_user_limit(self, username: str) -> int:
        # TODO: se username contém 'admin', 100, else 10
        if "admin" in username.lower():
            return 100
        return 10
