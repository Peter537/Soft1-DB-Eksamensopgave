import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
PASS = "mysecurepassword"

# Singleton Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=PASS)

def get_redis_client():
    return redis_client
