import redis
import json
from utils.loader import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_QUEUE
from utils.logger import log_event

def get_redis_connection():
    """Создаёт подключение к Redis."""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)

def push_to_redis(data):
    """Добавляет событие в очередь Redis и возвращает статус True/False."""
    try:
        r = get_redis_connection()
        r.rpush(REDIS_QUEUE, json.dumps(data))
        log_event(f"Добавлено в Redis: {data}")
        return True
    except Exception as e:
        log_event(f"Ошибка добавления в Redis: {e}", "error")
        return False
