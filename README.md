# get_tme_id
Telegram Bot to Get ID based on AIOGram

---

### **Описание Dockerfile:**
- Установка базового образа **Python версии 3.9**
- Установка рабочей директории
- Копирование файла **`requirements.txt`** внутрь образа
- Установка зависимостей, указанных в файле **`requirements.txt`**
- Копирование всех файлов и папок нашего приложения внутрь образа
- Запуск команды, которая выполнит запуск файла **`main.py`** при старте контейнера

---

### **main.py Description:**

> This code imports necessary modules from aiogram library and os module. It then retrieves the bot token from an environment variable and creates a Bot instance using the token. A Dispatcher instance is also created using the bot instance.

> The code defines a message handler for the **/start** command. When a user sends the **/start** command to the bot, the handler function sends a welcome message containing **the user ID and chat ID of the user** who sent the command. The message is formatted using **HTML tags** and sent back to the user.

> Finally, if the name of the script is **'main'**, the executor starts polling for new updates from the Telegram API using the Dispatcher instance, and skips any updates that were missed while the bot was offline.

---

<pre>
Hello, I'm Zero Bot =>
👤 user ID: 223322980
👥 chat ID: 223322980
</pre>


## Библиотеки Телеграм для Python:

- **aiogram**: Это современная асинхронная библиотека на базе aiohttp и предоставляет множество удобных инструментов для разработчиков.

- **python-telegram-bot**: Это одна из наиболее популярных библиотек с большим комьюнити и активной поддержкой. Она обеспечивает высокий уровень абстракции и множество функций. Документация также обширна.

- **Telepot**: Еще одна популярная библиотека, которая предлагает как синхронный, так и асинхронный способ взаимодействия с Telegram Bot API.

- **pyTelegramBotAPI**: Очень простая в использовании библиотека, которая подходит для быстрого создания простых ботов.

- **Telethon**: Эта библиотека отличается тем, что она не только для ботов, но и для работы с полным Telegram API (как для пользователей, так и для ботов). Это дает вам возможность делать гораздо больше, чем просто создавать ботов, так как вы можете интерактивно работать с Telegram на уровне пользователя.

- **Pyrogram**: Еще одна библиотека для работы с Telegram API для пользователей и ботов. Она имеет активное сообщество и постоянно обновляется.

- **Tamtam Bot SDK**: Это SDK для создания ботов в TamTam, который предоставляет функционал, аналогичный Telegram.

- **Aiotg**: Эта библиотека предназначена для создания асинхронных ботов с использованием asyncio. Она предлагает простой интерфейс для создания ботов.

## Простой Бот на других языках:

- **JavaScript (Node.js)**: С помощью библиотеки node-telegram-bot-api или Telegraf.

- **Go**: Используется библиотека telebot.

- **Java**: Существует несколько библиотек, например, TelegramBots.

- **C#**: Библиотека Telegram.Bot позволяет разрабатывать ботов на данном языке.

- **Ruby**: Библиотека telegram-bot-ruby позволяет создавать ботов на Ruby.
