import redis

redis_cli = None

def init_redis():
    global redis_cli
    if redis_cli is not None:
        return redis_cli
    redis_cli = redis.Redis(
        host='redis',
        port=6379,
    )
    return redis_cli