import redis
import json
import os
import random
from dotenv import load_dotenv

# Загружаем настройки
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "minecraft_queue")
REDIS_DB = int(os.getenv("REDIS_DB", 0))
OUTPUT_FILE = "redis_queue_output.txt"

# Возможные значения
SITES = ["Twitch", "Trovo", "GoodGame", "VKPlay", "YouTube", "Kick"]
EVENTS = [
    "donate", "music", "new_follower", "raid", "skip_music", "stream_message", "launch",
    "mob", "moobs", "mooobs", "rnd_bag", "rnd_effect", "rnd_fluid", "rnd_schematic",
    "rtp", "command"
]
CURRENCIES = ["USD", "EUR", "RUB", "UAH", "KZT", "GBP"]
NAMES = ["Steve", "Alex", "Herobrine", "Notch", "Dream", "Technoblade", "Philza", "TommyInnit"]

def get_random_name():
    """Возвращает случайное имя."""
    return random.choice(NAMES)

def get_random_text():
    """Возвращает случайный текст."""
    texts = [
        "Привет!", "Как дела?", "Этот сервер классный!", "Можно с вами поиграть?",
        "Когда следующий стрим?", "Лучшая игра!", "Я люблю Minecraft!"
    ]
    return random.choice(texts)

def generate_random_event():
    """Генерирует случайное событие."""
    event = random.choice(EVENTS)
    site = random.choice(SITES)
    viewer_name = get_random_name()

    event_data = {
        "site": site,
        "event": event,
        "user": viewer_name
    }

    if event == "donate":
        event_data.update({
            "text": get_random_text() if random.random() > 0.3 else None,
            "donate": round(random.uniform(1, 100), 2),
            "currency": random.choice(CURRENCIES)
        })
    elif event == "music":
        event_data["text"] = f"https://youtube.com/watch?v=dQw4w9WgXcQ"
    elif event == "raid":
        event_data["qty"] = random.randint(5, 500)
    elif event in ["stream_message", "command"]:
        event_data["text"] = get_random_text()

    return event_data

def export_redis_queue():
    """Читает все элементы из очереди Redis и сохраняет в файл без удаления."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
        queue_items = r.lrange(REDIS_QUEUE, 0, -1)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            for item in queue_items:
                decoded_item = json.loads(item)
                file.write(json.dumps(decoded_item, ensure_ascii=False, indent=4) + "\n")

        print(f"Экспорт завершен. Данные сохранены в {OUTPUT_FILE}")
    except Exception as e:
        print(f"Ошибка при выгрузке данных из Redis: {e}")

def clear_redis_queue():
    """Очищает всю очередь Redis."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
        r.delete(REDIS_QUEUE)
        print("Очередь успешно очищена!")
    except Exception as e:
        print(f"Ошибка при очистке Redis: {e}")

def fill_redis_queue(count=10):
    """Заполняет очередь Redis случайными данными."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
        for _ in range(count):
            event_data = generate_random_event()
            r.rpush(REDIS_QUEUE, json.dumps(event_data))
            print(f"Добавлено в Redis: {event_data}")
        print(f"✅ Добавлено {count} случайных событий в очередь Redis!")
    except Exception as e:
        print(f"Ошибка при заполнении Redis: {e}")

def main():
    """Выводит меню и обрабатывает выбор пользователя."""
    while True:
        print("\nВыберите действие:")
        print("1) Очистить всю очередь")
        print("2) Экспортировать всю очередь")
        print("3) Заполнить очередь случайными данными")
        print("0) Выход")
        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            clear_redis_queue()
        elif choice == "2":
            export_redis_queue()
        elif choice == "3":
            try:
                count = int(input("Сколько событий добавить? (по умолчанию 10): ").strip() or 10)
                fill_redis_queue(count)
            except ValueError:
                print("Ошибка: введите число!")
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
