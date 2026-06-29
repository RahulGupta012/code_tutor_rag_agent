import redis

redis_client = redis.Redis(
    # host="redis",  # Use the service name defined in docker-compose.yml
    host="localhost",  # Use the service name defined in docker-compose.yml
    port=6379,
    decode_responses=True
)