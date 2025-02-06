import sys
import json

from utils.helper import format_tellraw, get_viewer_declension
from utils.rcon import send_rcon_command
from utils.redis import push_to_redis
from utils.logger import log_event


def parse_args(args):
    """Парсит аргументы командной строки."""
    params = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            params[key] = value
    return params


def handle_event(event, site, player_name, text=None, donate=None, currency=None, qty=None, command=None):
    """Обрабатывает событие и записывает его в Redis."""
    if not event or not site or not player_name:
        log_event("Ошибка: отсутствуют обязательные параметры!", "error")
        return

    message = f"[{site}] {player_name}: "

    if event == "donate" and donate is not None and currency:
        message += f"Спасибо за донат {donate} {currency}!"
        if text is not None:
            message_tellraw = format_tellraw(event, site, player_name, text=text, donate=donate, currency=currency)
        else:
            message_tellraw = format_tellraw(event, site, player_name, donate=donate, currency=currency)
    elif event == "raid" and qty is not None:
        message += f"Рейд от {player_name} с {qty} {get_viewer_declension(qty)}!"
        message_tellraw = format_tellraw(event, site, player_name, qty=qty)
    elif event == "new_viewer":
        message += "Новый зритель присоединился!"
        message_tellraw = format_tellraw(event, site, player_name)
    elif event == "new_follower":
        message += "Новый подписчик присоединился!"
        message_tellraw = format_tellraw(event, site, player_name)
    elif event == "rnd_effect":
        message += "Наложение случайного эффекта!"
        message_tellraw = format_tellraw(event, site, player_name)
    elif event == "rnd_bag":
        message += "Выдача случайной сумочки!"
        message_tellraw = format_tellraw(event, site, player_name)
    elif event == "tellraw" and text:
        message += text
        message_tellraw = text
    else:
        log_event(f"Ошибка: некорректные параметры для события {event}", "error")
        return

    send_rcon_command(f'w LLIaMMaH {message}')
    send_rcon_command(message_tellraw)

    redis_data = {
        "site": site,
        "event": event,
        "user": player_name,
        "from": player_name,
        "text": text,
        "donate": donate,
        "currency": currency,
        "qty": qty,
        "command": command
    }
    push_to_redis(redis_data)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        log_event("Ошибка: недостаточно аргументов! Требуются event, site, player_name.", "error")
        sys.exit(1)

    params = parse_args(sys.argv[1:])

    event = params.get("event")
    site = params.get("site")
    player_name = params.get("player_name")
    text = params.get("text")
    donate = float(params.get("donate")) if "donate" in params else None
    currency = params.get("currency")
    qty = int(params.get("qty")) if "qty" in params else None
    command = params.get("command")

    log_event(f"Скрипт запущен с параметрами: {params}")
    handle_event(event, site, player_name, text, donate, currency, qty, command)
