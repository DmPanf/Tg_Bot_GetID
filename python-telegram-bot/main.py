import os
import configparser
from datetime import datetime
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists('bot_config.ini'):
        raise FileNotFoundError("bot_config.ini not found!")
    config.read('bot_config.ini')
    try:
        log_file = config['LOGS']['path']
    except KeyError:
        log_file = "./logs/default_log.txt"  # значение по умолчанию, если не найдено в конфиге

    load_dotenv()
    TOKEN = os.environ.get("TG_TOKEN")
    if not TOKEN:
        raise ValueError("TG_TOKEN is not set in the environment variables or .env file!")

    return TOKEN, log_file

def log_message(update: Update, log_file: str):
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user = update.message.from_user
    chat = update.message.chat

    log_text = (f"🔸 {current_time} | User ID: {user.id} | Username: {user.username} | "
                f"First Name: {user.first_name} | Last Name: {user.last_name} | "
                f"Language: {user.language_code} | Chat ID: {chat.id} | "
                f"Chat Type: {chat.type} | Text: {update.message.text}\n")

    with open(log_file, "a") as file:
        file.write(log_text)

def start(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    update.message.reply_text(
        f"Hello, I'm Zero Bot =>\n"
        f"👤 <b>user ID:</b> <code>{user.id}</code>\n"
        f"👥 <b>chat ID:</b> <code>{update.message.chat.id}</code>",
        parse_mode=ParseMode.HTML
    )
    log_message(update, LOG_PATH)

def main() -> None:
    TOKEN, LOG_PATH = load_config()
    updater = Updater(token=TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
