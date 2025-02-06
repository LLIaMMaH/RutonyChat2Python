import psycopg2
from utils.loader import PG_HOST, PG_PORT, PG_DATABASE, PG_USER, PG_PASSWORD
from utils.logger import log_event


def get_db_connection():
    """Создаёт подключение к PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWORD
        )
        return conn
    except Exception as e:
        log_event(f"Ошибка подключения к PostgreSQL: {e}", "error")
        return None


def save_event_to_db(event_data):
    """Сохраняет событие в PostgreSQL."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            sql = """
                INSERT INTO events (event_type, site, player_name, text, donate, currency, qty, redis, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            cur.execute(sql, (
                event_data["event"],
                event_data["site"],
                event_data["user"],
                event_data["text"],
                event_data["donate"],
                event_data["currency"],
                event_data["qty"],
                event_data["redis"]
            ))
        conn.commit()
        log_event("Запись успешно сохранена в PostgreSQL.")
    except Exception as e:
        log_event(f"Ошибка при записи в PostgreSQL: {e}", "error")
    finally:
        conn.close()
