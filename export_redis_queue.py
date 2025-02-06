import redis
import json
import os
from dotenv import load_dotenv

# Загружаем настройки
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "minecraft_queue")
REDIS_DB = int(os.getenv("REDIS_DB", 0))
OUTPUT_FILE = "redis_queue_output.txt"


def export_redis_queue():
    """Читает все элементы из очереди Redis и сохраняет в файл без удаления."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
        queue_items = r.lrange(REDIS_QUEUE, 0, -1)  # Читаем всю очередь без удаления

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            for item in queue_items:
                decoded_item = json.loads(item)
                file.write(json.dumps(decoded_item, ensure_ascii=False, indent=4) + "\n")

        print(f"Экспорт завершен. Данные сохранены в {OUTPUT_FILE}")
    except Exception as e:
        print(f"Ошибка при выгрузке данных из Redis: {e}")


if __name__ == "__main__":
    export_redis_queue()
