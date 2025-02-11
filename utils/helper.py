def get_viewer_declension(qty):
    """
    Возвращает правильное склонение слова 'зритель' в зависимости от числа.

    :param qty: Количество зрителей.
    :return: Строка со словом в правильном склонении.
    """
    titles = ["зритель", "зрителя", "зрителей"]
    cases = [2, 0, 1, 1, 1, 2]

    return titles[2 if 11 <= qty % 100 <= 19 else cases[5 if qty % 10 >= 5 else qty % 10]]


def format_tellraw(site, event, viewer_name, user_name=None, text=None, donate=None, currency=None, qty=None):
    """
    Формирует команду `tellraw` для RCON в зависимости от типа события.

    :param site: Платформа (Twitch, Trovo и т. д.).
    :param event: Тип события (raid, donate, new_viewer, new_follower).
    :param viewer_name: Имя зрителя.
    :param user_name: Имя игрока.
    :param text: Дополнительный текст.
    :param donate: Сумма доната.
    :param currency: Валюта доната.
    :param qty: Количество зрителей (для рейда).
    :return: Строка команды tellraw.
    """

    if site is None:
        site='RC2P'

    base = [
        "", {"text": "["}, {"text": site, "color": "yellow"}, {"text": "] "}
    ]

    if event == "donate":
        base.extend([
            {"text": viewer_name, "color": "aqua"},
            {"text": " только что задонатил "}, {"text": str(donate), "color": "gold"},
            {"text": f" {currency}!"}
        ])

        if text is not None:
            base.extend([
                {"text": " А вот, что он написал: "}, {"text": text, "color": "gold"}
            ])
    elif event == "music":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " заказал музыку."}
        ])
    elif event == "new_follower":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " теперь отслеживает."}
        ])
    elif event == "new_viewer":
        base.extend([
            {"text": "Новый зритель "}, {"text": viewer_name, "color": "aqua"},
            {"text": "."}
        ])
    elif event == "raid":
        viewers = get_viewer_declension(qty)
        base.extend([
            {"text": "Рейд от "}, {"text": viewer_name, "color": "aqua"},
            {"text": "! С ним приходит "}, {"text": str(qty), "color": "gold"},
            {"text": f" {viewers}."}
        ])
    elif event == "skip_music":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " скипнул трек с плейлисте."}
        ])
    elif event == "stream_message":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": ": ", "color": "yellow"}, {"text": text}
        ])
    elif event == "tellraw":
        base.extend([
            {"text": text}
        ])
    elif event == "command":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " выполняет команду "}, {"text": text, "color": "yellow"}
        ])
    elif event == "launch":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " подкидывает на случайное число блоков. "}
        ])
    elif event == "mob":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " призывает случайного моба. "}
        ])
    elif event == "moobs":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " призывает несколько случайных мобов. "}
        ])
    elif event == "mooobs":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " призывает много случайных мобов. "}
        ])
    elif event == "rnd_bag":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " дарит случайную сумочку."}
        ])
    elif event == "rnd_effect":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " накладывает случайный эффект."}
        ])
    elif event == "rnd_fluid":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " заливает случайной жидкостью."}
        ])
    elif event == "rnd_schematic":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " замуровывает в случайную схематику."}
        ])
    elif event == "rtp":
        base.extend([
            {"text": viewer_name, "color": "aqua"}, {"text": " закидывает в случайные координаты."}
        ])
    else:
        base.extend([
            {"text": " Что-то пошло не так."}
        ])

    return f'tellraw LLIaMMaH {base}'
