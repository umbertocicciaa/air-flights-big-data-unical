redis_cli = None

def init_redis():
    if redis_cli is not None:
        return redis_cli
    redis_cli = redis.Redis(
        host='redis',
        port=6379,
        charset="utf-8",
        decode_responses=True
    )
    return redis_cli