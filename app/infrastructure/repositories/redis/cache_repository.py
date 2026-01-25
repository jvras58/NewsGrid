import hashlib
import json
from typing import Any

from app.domain.report.repositories import ICacheRepository
from app.infrastructure.cache.redis_client import get_redis_client
from utils.settings import settings


class RedisCacheRepository(ICacheRepository):
    def make_cache_key(self, topic: str, params: dict[str, Any] | None = None) -> str:
        normalized_topic = topic.lower().strip()
        key_data = f"topic:{normalized_topic}"
        if params:
            sorted_params = json.dumps(params, sort_keys=True)
            key_data += f":{sorted_params}"
        return f"report_cache:{hashlib.sha256(key_data.encode()).hexdigest()}"

    def get_cached_report(self, cache_key: str) -> dict[str, Any] | None:
        client = get_redis_client()
        data = client.get(cache_key)
        if data:
            return json.loads(data)
        return None

    def set_cached_report(self, cache_key: str, report: dict[str, Any]) -> bool:
        client = get_redis_client()
        return client.setex(
            cache_key, settings.report_cache_ttl_seconds, json.dumps(report)
        )
