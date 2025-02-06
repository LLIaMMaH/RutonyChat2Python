import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

def get_env_variable(key, default=None, required=False):
    """Получает переменную окружения, проверяя на обязательность."""
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(f"Переменная окружения {key} обязательна, но не задана!")
    return value

# Настройки RCON
RCON_HOST = get_env_variable("RCON_HOST", "localhost")
RCON_PORT = int(get_env_variable("RCON_PORT", 25575))
RCON_PASSWORD = get_env_variable("RCON_PASSWORD", required=True)

# Настройки Redis
REDIS_HOST = get_env_variable("REDIS_HOST", "localhost")
REDIS_PORT = int(get_env_variable("REDIS_PORT", 6379))
REDIS_PASSWORD = get_env_variable("REDIS_PASSWORD", None)
REDIS_DB = int(get_env_variable("REDIS_DB", 0))
REDIS_QUEUE = get_env_variable("REDIS_QUEUE", "minecraft_queue")
REDIS_PROCESSING_QUEUE = get_env_variable("REDIS_PROCESSING_QUEUE", "minecraft_queue_processing")

# Настройки PostgreSQL
PG_HOST = get_env_variable("PG_HOST", "localhost")
PG_PORT = get_env_variable("PG_PORT", "5432")
PG_DATABASE = get_env_variable("PG_DATABASE", "minecraft_events")
PG_USER = get_env_variable("PG_USER", "postgres")
PG_PASSWORD = get_env_variable("PG_PASSWORD", "yourpassword")

# Настройки логирования
LOG_FILE = get_env_variable("LOG_FILE", "script.log")
LOG_LEVEL = get_env_variable("LOG_LEVEL", "INFO")
