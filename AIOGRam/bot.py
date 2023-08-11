# Этот бот в ответ на команду /start, отправленную ему пользователем, возвращает приветственное сообщение, 
# а также идентификатор пользователя (user ID) и идентификатор чата (chat ID).
# Функция load_config читает конфигурационный файл и загружает переменные окружения.
# Функция log_message записывает информацию о полученных сообщениях в файл лога, который указан в конфигурации.
# При обработке сообщения /start сначала отправляется приветственное сообщение, а затем вызывается функция логирования.

import os
import configparser
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

def load_config():
    """Загрузка конфигурации из bot_config.ini и переменных окружения."""
    config = configparser.ConfigParser()
    config.read('bot_config.ini')
    
    TOKEN = os.environ.get("TG_TOKEN")
    log_file = config['LOGS']['path']
    
    return TOKEN, log_file

def log_message(message: types.Message, log_file: str):
    """Логирование входящего сообщения в указанный файл."""
    with open(log_file, "a") as file:
        log_text = (f"User ID: {message.from_user.id}\n"
                    f"Chat ID: {message.chat.id}\n"
                    f"Text: {message.text}\n\n")
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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
