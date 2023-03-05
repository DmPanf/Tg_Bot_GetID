from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # my_str = f"Hello, I'm Zero Bot =>\n👤 **user ID:** `{message.from_user.id}`\n👥 **chat ID:** `{message.chat.id}`"
    my_str = f"Hello, I'm Zero Bot =>\n👤 <b>user ID:</b> <code>{message.from_user.id}</code>\n👥 <b>chat ID:</b> <code>{message.chat.id}</code>"
    # возвращает user ID и chat ID
    # await message.reply(my_str, parse_mode="Markdown")
    await message.reply(my_str, parse_mode="HTML")

if __name__ == '__main__':
    # запускает бота
    executor.start_polling(dp, skip_updates=True)
