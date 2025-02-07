from datetime import datetime
import sys
from utils.helper import format_tellraw, get_viewer_declension
from utils.rcon import send_rcon_command
from utils.redis import push_to_redis
from utils.database import save_event_to_db
from utils.logger import log_event


def parse_args(args):
    """Парсит аргументы командной строки."""
    params = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            params[key] = value
    return params


def handle_event(event, site, viewer_name, text=None, donate=None, currency=None, qty=None, command=None):
    """Обрабатывает событие, отправляет в RCON, Redis и PostgreSQL."""
    if not event or not site or not viewer_name:
        log_event("Ошибка: отсутствуют обязательные параметры!", "error")
        return

    message = f"[{site}] {viewer_name}: "

    if event == "donate" and donate is not None and currency:
        message += f"Спасибо за донат {donate} {currency}!"
        message_tellraw = format_tellraw(event, site, viewer_name, text=text, donate=donate, currency=currency)
    elif event == "raid" and qty is not None:
        message += f"Рейд от {viewer_name} с {qty} {get_viewer_declension(qty)}!"
        message_tellraw = format_tellraw(event, site, viewer_name, qty=qty)
    elif event == "new_viewer":
        message += "Новый зритель присоединился!"
        message_tellraw = format_tellraw(event, site, viewer_name)
    elif event == "new_follower":
        message += "Новый подписчик присоединился!"
        message_tellraw = format_tellraw(event, site, viewer_name)
    elif event == "rnd_effect":
        message += "Наложение случайного эффекта!"
        message_tellraw = format_tellraw(event, site, viewer_name)
    elif event == "rnd_bag":
        # TODO: Для отладки выставляем в текст дату, чтобы анализировать очередь в Redis
        if text is None:
            current_datetime = datetime.now()
            text = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        message += "Выдача случайной сумочки!"
        message_tellraw = format_tellraw(event, site, viewer_name)
    elif event == "music":
        message += "Заказ музыки!"
        message_tellraw = format_tellraw(event, site, viewer_name)
    elif event == "skip_music":
        message += "Пропуск трека из списка!"
        message_tellraw = format_tellraw(event, site, viewer_name)
    elif event == "new_message":
        message += "Новое сообщение в чате!"
        message_tellraw = format_tellraw(event, site, viewer_name, text=text)
    elif event == "tellraw" and text:
        message += text
        message_tellraw = text
    else:
        log_event(f"Ошибка: некорректные параметры для события {event}", "error")
        return

    # send_rcon_command(f'w LLIaMMaH {message}')
    send_rcon_command(message_tellraw)

    redis_status = push_to_redis({
        "site": site,
        "event": event,
        "user": viewer_name,
        "text": text,
        "donate": donate,
        "currency": currency,
        "qty": qty,
        "command": command
    })

    event_data = {
        "site": site,
        "event": event,
        "user": viewer_name,
        "text": text,
        "donate": donate,
        "currency": currency,
        "qty": qty,
        "redis": redis_status
    }

    save_event_to_db(event_data)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        log_event("Ошибка: недостаточно аргументов! Требуются event, site, viewer_name.", "error")
        sys.exit(1)

    params = parse_args(sys.argv[1:])

    event = params.get("event")
    site = params.get("site")
    viewer_name = params.get("viewer_name")
    text = params.get("text")
    donate = float(params.get("donate")) if "donate" in params else None
    currency = params.get("currency")
    qty = int(params.get("qty")) if "qty" in params else None
    command = params.get("command")

    log_event(f"Скрипт запущен с параметрами: {params}")
    handle_event(event, site, viewer_name, text, donate, currency, qty, command)
