# Этот бот в ответ на команду /start, отправленную ему пользователем, возвращает приветственное сообщение, 
# а также идентификатор пользователя (user ID) и идентификатор чата (chat ID).
# Функция load_config читает конфигурационный файл и загружает переменные окружения.
# Функция log_message записывает информацию о полученных сообщениях в файл лога, который указан в конфигурации.
# При обработке сообщения /start сначала отправляется приветственное сообщение, а затем вызывается функция логирования.

import os
import configparser
from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
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
    if not TOKEN:
        raise ValueError("TG_TOKEN is not set in the environment variables or .env file!")

    return TOKEN, log_file


def log_message(message: types.Message, log_file: str):
    """Логирование входящего сообщения в указанный файл."""
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Проверяем существование папки и создаем, если необходимо
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    user_info = (f"{message.date.strftime('%Y-%m-%d %H:%M:%S')} | "
                 f"User ID: {message.from_user.id} | "
                 f"Username: {message.from_user.username} | "
                 f"First Name: {message.from_user.first_name} | "
                 f"Last Name: {message.from_user.last_name} | "
                 f"Language: {message.from_user.language_code}")
    
    chat_info = (f"Chat Type: {message.chat.type} | "
                 f"Chat ID: {message.chat.id} | "
                 f"Chat Title: {message.chat.title or 'N/A'}")

    log_text = f"🔹{user_info} | Chat Info: [{chat_info}] | Message Text: {message.text}\n"
     
    with open(log_file, "a") as file:
        file.write(log_text)

# Загружаем конфигурацию
TOKEN, LOG_PATH = load_config()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    my_str = (f"Hello, I'm Zero Bot =>\n"
              f"👤 <b>user ID:</b> <code>{message.from_user.id}</code>\n"
              f"👥 <b>chat ID:</b> <code>{message.chat.id}</code>")
    
    await message.reply(my_str, parse_mode="HTML")
    log_message(message, LOG_PATH)

@dp.message_handler(lambda message: message.forward_from)
async def handle_forwarded_message(message: types.Message):
    original_user_id = message.forward_from.id
    chat_id = message.chat.id

    response_str = (f"👤 <b>Original User ID (from forwarded message):</b> <code>{original_user_id}</code>\n"
                    f"👥 <b>Chat ID:</b> <code>{chat_id}</code>")
    
    await message.reply(response_str, parse_mode="HTML")
    log_message(message, LOG_PATH)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
