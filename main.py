import sys
import json
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


def get_viewer_declension(qty):
    """Определяет правильное склонение слова 'зритель'."""
    qty = int(qty)
    if 11 <= qty % 100 <= 19:
        return "зрителей"
    last_digit = qty % 10
    if last_digit == 1:
        return "зритель"
    elif 2 <= last_digit <= 4:
        return "зрителя"
    else:
        return "зрителей"


def handle_event(event, site, player_name, text=None, donate=None, currency=None, qty=None, command=None):
    """Обрабатывает событие и записывает его в Redis."""
    if not event or not site or not player_name:
        log_event("Ошибка: отсутствуют обязательные параметры!", "error")
        return

    message = f"[{site}] {player_name}: "

    if event == "donate" and donate is not None and currency:
        message += f"Спасибо за донат {donate} {currency}!"
    elif event == "raid" and qty is not None:
        message += f"Рейд от {player_name} с {qty} {get_viewer_declension(qty)}!"
    elif event == "new_viewer":
        message += "Новый зритель присоединился!"
    elif event == "tellraw" and text:
        message += text
    else:
        log_event(f"Ошибка: некорректные параметры для события {event}", "error")
        return

    send_rcon_command(f'w LLIaMMaH {message}')

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
