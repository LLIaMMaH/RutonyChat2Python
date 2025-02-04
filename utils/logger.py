from loguru import logger
from utils.loader import LOG_FILE, LOG_LEVEL

# Настройка логирования в файл
logger.add(LOG_FILE, rotation="10MB", level=LOG_LEVEL, format="{time} {level} {message}")

def log_event(message, level="info"):
    """Записывает событие в лог-файл."""
    if level == "error":
        logger.error(message)
    elif level == "warning":
        logger.warning(message)
    else:
        logger.info(message)
