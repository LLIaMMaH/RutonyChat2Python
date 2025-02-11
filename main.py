from datetime import datetime
import sys
from utils.helper import format_tellraw, get_viewer_declension
from utils.rcon import send_rcon_command
from utils.redis import push_to_redis
from utils.database import save_event_to_db
from utils.logger import log_event

# Определяем, какие события куда записывать. Если событие тут не указано, значит оно будет добавлено в оба места.
EVENT_STORAGE_RULES = {
    # Записываем только в базу данных PostgreSQSL
    "donate": "postgres",
    "music": "postgres",
    "new_follower": "postgres",
    "new_viewer": "postgres",
    "raid": "postgres",
    "skip_music": "postgres",
    "stream_message": "postgres",
    "tellraw": "postgres",

    # Записываем только в очередь Redis

    # Записываем в оба места
    # "command": "redis",
    # "launch": "redis",
    # "mob": "redis",
    # "moobs": "redis",
    # "mooobs": "redis",
    # "rnd_bag": "redis",
    # "rnd_effect": "redis",
    # "rnd_fluid": "redis",
    # "rnd_schematic": "redis",
    # "rtp": "redis",
}


def parse_args(args):
    """Парсит аргументы командной строки."""
    params = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            params[key] = value
    return params


def handle_event(site, event, viewer_name, user_name=None, text=None, donate=None, currency=None, qty=None, command=None):
    """Обрабатывает событие, отправляет в RCON, Redis и PostgreSQL."""
    if not site or not event or not viewer_name:
        log_event("Ошибка: отсутствуют обязательные параметры!", "error")
        return

    message = f"[{site}] {viewer_name}: "

    # Донат
    if event == "donate" and donate is not None and currency:
        message_tellraw = format_tellraw(site, event, viewer_name, text=text, donate=donate, currency=currency)

    # Заказ музыки
    elif event == "music":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Новый подписчик присоединился
    elif event == "new_follower":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Новый зритель присоединился
    elif event == "new_viewer":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Рейд от стримера
    elif event == "raid" and qty is not None:
        message_tellraw = format_tellraw(site, event, viewer_name, qty=qty)

    # Пропуск трека из списка заказов
    elif event == "skip_music":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Новое сообщение в чате
    elif event == "stream_message":
        message_tellraw = format_tellraw(site, event, viewer_name, text=text)

    # Отправить в игру сообщение в формате tellraw
    elif event == "tellraw" and text:
        message_tellraw = format_tellraw(site, event, viewer_name, text=text)

    # Выполнить команду
    elif event == "command":
        if text is not None:
            # TODO: Проверка, что у нас команда, которую мы знаем.
            message_tellraw = format_tellraw(site, event, viewer_name, text=text)
            send_rcon_command(text)

    # Подкинуть стримера на случайное число блоков вверх
    elif event == "launch":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Заспавнить рядом со стримером случайного моба
    elif event == "mob":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Заспавнить рядом со стримером случайных мобов (от 1 до 5)
    elif event == "moobs":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Заспавнить рядом со стримером случайных мобов (от 5 до 20)
    elif event == "mooobs":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Выдача случайной сумочки
    elif event == "rnd_bag":
        # TODO: Для отладки выставляем в текст дату, чтобы анализировать очередь в Redis
        if text is None:
            current_datetime = datetime.now()
            text = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Наложение случайного эффекта
    elif event == "rnd_effect":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Разлить вокруг стримера случайную жидкость
    elif event == "rnd_fluid":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Замуровать стримера в случайную схематику
    elif event == "rnd_schematic":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Телепортируем стримера в случайные координаты
    elif event == "rtp":
        message_tellraw = format_tellraw(site, event, viewer_name)

    # Не известное событие
    else:
        log_event(f"Ошибка: некорректные параметры для события {event}", "error")
        return

    # send_rcon_command(f'w LLIaMMaH {message}')
    send_rcon_command(message_tellraw)

    # Проверяем, куда записывать событие
    storage_rule = EVENT_STORAGE_RULES.get(event, "both")

    redis_data = push_to_redis({
        "site": site,
        "event": event,
        "from": viewer_name,
        "user": user_name,
        "text": text,
        "donate": donate,
        "currency": currency,
        "qty": qty,
        "command": command
    })

    if storage_rule in ["redis", "both"]:
        redis_status = push_to_redis(redis_data)
    else:
        # redis_status = False if storage_rule == "postgres" else None
        redis_status = None

    if storage_rule in ["postgres", "both"]:
        event_data = {**redis_data, "redis": redis_status}
        save_event_to_db(event_data)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        log_event("Ошибка: недостаточно аргументов! Требуются site, event, viewer_name.", "error")
        sys.exit(1)

    params = parse_args(sys.argv[1:])

    site = params.get("site")
    event = params.get("event")
    viewer_name = params.get("viewer_name")
    user_name = params.get("user_name")
    text = params.get("text")
    donate = float(params.get("donate")) if "donate" in params else None
    currency = params.get("currency")
    qty = int(params.get("qty")) if "qty" in params else None
    command = params.get("command")

    log_event(f"Скрипт запущен с параметрами: {params}")
    handle_event(site, event, viewer_name, user_name, text, donate, currency, qty, command)
