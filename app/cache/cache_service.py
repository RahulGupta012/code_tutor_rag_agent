import json
import hashlib

from app.cache.redis_client import redis_client


CACHE_EXPIRY = 3600


def generate_cache_key(query: str):

    return hashlib.md5(
        query.strip().lower().encode()
    ).hexdigest()


def get_cached_response(query: str):

    cache_key = generate_cache_key(query)

    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    return None


def cache_response(query: str, response: dict):

    cache_key = generate_cache_key(query)

    redis_client.set(
        cache_key,
        json.dumps(response),
        ex=CACHE_EXPIRY
    )