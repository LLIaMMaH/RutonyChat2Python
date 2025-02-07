# Rutony Chat to Python (Minecraft Stream Events Handler)

Скрипт - Костыль. Этот проект предназначен для записи информации о различных событиях с различных стриминговых платформ (Twitch, Trovo, GoodGame, VKPlay и др.) и их передачи в очередь событий в [Redis][Redis] и для хранения, анализа и статистики в базу данных [PostgreSQL][PostgreSQL]. Дополнительно скрипт отправляет сообщения о событии в **Minecraft** через **RCON**.  

[Почему так?](./WhyIsThat.md)  


## **📌 Функциональность**
- Получает параметры события из командной строки.
- Записывает информацию о событии в очередь [Redis][Redis].
- Записывает информацию о событии в базу данных [PostgreSQL][PostgreSQL].
- В зависимости от типа события отправляет команду в **Minecraft** (RCON).
- Логирует все действия в файл (`loguru`).
- Поддерживает конфигурацию через **.env**.

### **Поддерживаемые параметры**
| Параметр      | Тип   | Обязателен | Описание                                                      |
|---------------|---| --- |---------------------------------------------------------------|
| `event`       | str | ✅ | Тип события: `donate`, `raid`, `new_viewer`, `tellraw`, `...` |
| `site`        | str | ✅ | Платформа: `Twitch`, `Trovo`, `VKPlay`, `GoodGame`, `...`     |
| `viewer_name` | str | ✅ | Ник зрителя на стриминговой платформе                         |
| `text`        | str | ❌ | Текст сообщения                                               |
| `donate`      | float | ❌ | Сумма доната                                                  |
| `currency`    | str | ❌ | Валюта доната                                                 |
| `qty`         | int | ❌ | Количество зрителей при рейде                                 |
| `command`     | str | ❌ | Minecraft-команда для выполнения                              |

---

## **📦 Установка**

### **1. Установите Python 3.8+**  
Скачайте и установите Python, если он не установлен:  
[https://www.python.org/downloads/](https://www.python.org/downloads/)

### **2. Установите зависимости**  
Склонируйте репозиторий и установите зависимости:  
```sh
git clone https://github.com/LLIaMMaH/RutonyChat2Python.git
cd RutonyChat2Python
pip install -r requirements.txt
```

### **3. PostgreSQL**
Создать базу данных.  
<details>
  <summary>Создать таблицу.</summary>

```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    site TEXT NOT NULL,
    viewer_name TEXT NOT NULL,
    text TEXT,
    donate NUMERIC,
    currency TEXT,
    qty INT,
    redis BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);
```
</details>


---
**PS:** Поскольку скрипт просто вызывается, то необходимо установить нужные зависимости в глобальное хранилище.


[//]: # (Short links)
[Redis]: https://redis.io/ "Redis"
[PostgreSQL]: https://www.postgresql.org/ "PostgreSQL: The World's Most Advanced Open Source Relational Database"