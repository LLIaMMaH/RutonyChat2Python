import os
from loguru import logger
from utils.loader import LOG_FILE, LOG_LEVEL

# Очищаем все предыдущие обработчики логирования
logger.remove()

# Настройка логирования в файл
log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)  # Создаём папку для логов, если её нет

# Настройка логирования в файл
logger.add(LOG_FILE, rotation="10MB", level=LOG_LEVEL, format="{time} {level} {message}", enqueue=True, backtrace=True, diagnose=True)


def log_event(message, level="info"):
    """Записывает событие в лог-файл."""
    if level == "error":
        logger.error(message)
    elif level == "warning":
        logger.warning(message)
    else:
        logger.info(message)
