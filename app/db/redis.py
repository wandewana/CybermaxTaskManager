import redis.asyncio as redis

# Connection details for the Redis service running in Docker
REDIS_URL = "redis://localhost:6379"

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def get_redis_client():
    """Dependency to get a Redis client."""
    return redis_client
