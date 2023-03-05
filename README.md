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
