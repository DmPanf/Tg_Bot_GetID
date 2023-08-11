import os
import configparser
from datetime import datetime
from pyrogram import Client, filters
from dotenv import load_dotenv

def load_config():
    """Загрузка конфигурации из bot_config.ini и переменных окружения."""
    config = configparser.ConfigParser()
    if not os.path.exists('bot_config.ini'):
        raise FileNotFoundError("bot_config.ini not found!")
    config.read('bot_config.ini')
    try:
        log_file = config['LOGS']['path']
    except KeyError:
        log_file = "./logs/default_log.txt"  # значение по умолчанию, если не найдено в конфиге

    load_dotenv()  # загрузка переменных окружения из файла .env
    TOKEN = os.environ.get("TG_TOKEN")
    APP_ID = os.environ.get("TG_APP_ID") # нужен для Pyrogram
    APP_HASH = os.environ.get("TG_APP_HASH") # нужен для Pyrogram
    if not TOKEN or not APP_ID or not APP_HASH:
        raise ValueError("TG_TOKEN, TG_APP_ID, or TG_APP_HASH is not set in the environment variables or .env file!")

    return TOKEN, APP_ID, APP_HASH, log_file

def log_message(message, log_file: str):
    """Логирование входящего сообщения в указанный файл."""
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_info = (f"{current_time} | "
                 f"User ID: {message.from_user.id} | "
                 f"Username: {message.from_user.username or 'N/A'} | "
                 f"First Name: {message.from_user.first_name} | "
                 f"Last Name: {message.from_user.last_name or 'N/A'}")

    chat_info = (f"Chat Type: {message.chat.type} | "
                 f"Chat ID: {message.chat.id}")

    log_text = f"🔹{user_info} | Chat Info: [{chat_info}] | Message Text: {message.text}\n"

    with open(log_file, "a") as file:
        file.write(log_text)

# Загружаем конфигурацию
TOKEN, APP_ID, APP_HASH, LOG_PATH = load_config()

app = Client("my_bot", bot_token=TOKEN, api_id=APP_ID, api_hash=APP_HASH)

@app.on_message(filters.command("start"))
async def start(client, message):
    my_str = (f"Hello, I'm Zero Bot =>\n"
              f"👤 <b>user ID:</b> <code>{message.from_user.id}</code>\n"
              f"👥 <b>chat ID:</b> <code>{message.chat.id}</code>")

    await message.reply(my_str, parse_mode="HTML")
    log_message(message, LOG_PATH)

@app.on_message(filters.forwarded)
async def handle_forwarded_message(client, message):
    original_user_id = message.forward_from.id
    chat_id = message.chat.id

    response_str = (f"👤 <b>Original User ID (from forwarded message):</b> <code>{original_user_id}</code>\n"
                    f"👥 <b>Chat ID:</b> <code>{chat_id}</code>")

    await message.reply(response_str, parse_mode="HTML")
    log_message(message, LOG_PATH)

if __name__ == "__main__":
    app.run()
