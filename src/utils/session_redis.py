import os
import redis
import json

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_db: int = int(os.getenv('REDIS_DB', 0))

r = redis.Redis(host=redis_host, port=6379, db=redis_db)

def get_client():
    return r

def get_from_cache(key):
    value = r.get(key)
    if value is not None:
        return json.loads(value)
    return None

def save_to_cache(key, value, expiration=None):
    serialized_value = json.dumps(value)
    if expiration:
        r.setex(key, expiration, serialized_value)
    else:
        r.set(key, serialized_value)