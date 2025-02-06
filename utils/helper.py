# def get_viewer_declension(qty):
#     """Определяет правильное склонение слова 'зритель'."""
#     qty = int(qty)
#     if 11 <= qty % 100 <= 19:
#         return "зрителей"
#     last_digit = qty % 10
#     if last_digit == 1:
#         return "зритель"
#     elif 2 <= last_digit <= 4:
#         return "зрителя"
#     else:
#         return "зрителей"


def get_viewer_declension(qty):
    """
    Возвращает правильное склонение слова 'зритель' в зависимости от числа.

    :param qty: Количество зрителей.
    :return: Строка со словом в правильном склонении.
    """
    titles = ["зритель", "зрителя", "зрителей"]
    cases = [2, 0, 1, 1, 1, 2]

    return titles[2 if 11 <= qty % 100 <= 19 else cases[5 if qty % 10 >= 5 else qty % 10]]


def format_tellraw(event, site, player_name, text=None, donate=None, currency=None, qty=None):
    """
    Формирует команду `tellraw` для RCON в зависимости от типа события.

    :param event: Тип события (raid, donate, new_viewer, new_follower).
    :param site: Платформа (Twitch, Trovo и т. д.).
    :param player_name: Имя игрока.
    :param text: Дополнительный текст.
    :param donate: Сумма доната.
    :param currency: Валюта доната.
    :param qty: Количество зрителей (для рейда).
    :return: Строка команды tellraw.
    """
    base = [
        "", {"text": "["}, {"text": site, "color": "yellow"}, {"text": "] "}
    ]
    # Стандаортные события на стриме
    if event == "raid":
        viewers = get_viewer_declension(qty)
        base.extend([
            {"text": "Рейд от "}, {"text": player_name, "color": "aqua"},
            {"text": "! С ним приходит "}, {"text": str(qty), "color": "gold"},
            {"text": f" {viewers}."}
        ])
    elif event == "donate":
        base.extend([
            {"text": player_name, "color": "aqua"},
            {"text": " только что задонатил "}, {"text": str(donate), "color": "gold"},
            {"text": f" {currency}!"}
        ])
        if text is not None:
            base.extend([
                {"text": " А вот, что он написал: "}, {"text": text, "color": "gold"}
            ])
    elif event == "new_viewer":
        base.extend([
            {"text": "Новый зритель "}, {"text": player_name, "color": "aqua"},
            {"text": "."}
        ])
    elif event == "new_follower":
        base.extend([
            {"text": player_name, "color": "aqua"}, {"text": " теперь отслеживает."}
        ])
    # Далее идут шалости
    elif event == "rnd_effect":
        base.extend([
            {"text": player_name, "color": "aqua"}, {"text": " накладывает случайный эффект."}
        ])
    elif event == "rnd_bag":
        base.extend([
            {"text": player_name, "color": "aqua"}, {"text": " дарит случайную сумочку."}
        ])
    else:
        return None  # Если событие неизвестное, возвращаем None

    return f'tellraw LLIaMMaH {base}'
