import os
import configparser
from datetime import datetime
from aiotg import Bot, Chat
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

def log_message(message, log_file: str):
    """Логирование входящего сообщения в указанный файл."""
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    user_info = (f"{current_time} | "
                 f"User ID: {message['from']['id']} | "
                 f"Username: {message['from'].get('username', 'N/A')} | "
                 f"First Name: {message['from']['first_name']} | "
                 f"Last Name: {message['from'].get('last_name', 'N/A')}")

    chat_info = (f"Chat Type: {message['chat']['type']} | "
                 f"Chat ID: {message['chat']['id']}")

    log_text = f"🔹{user_info} | Chat Info: [{chat_info}] | Message Text: {message['text']}\n"
     
    with open(log_file, "a") as file:
        file.write(log_text)

# Загружаем конфигурацию
TOKEN, LOG_PATH = load_config()

bot = Bot(api_token=TOKEN)

@bot.command("/start")
async def start(chat: Chat, match):
    my_str = (f"Hello, I'm Zero Bot =>\n"
              f"👤 <b>user ID:</b> <code>{chat.sender['id']}</code>\n"
              f"👥 <b>chat ID:</b> <code>{chat.id}</code>")
    
    await chat.reply(my_str, parse_mode="HTML")
    log_message(chat.message, LOG_PATH)

# Aiotg не предоставляет готового способа определить, было ли сообщение переслано.
# Вам, возможно, потребуется выполнить дополнительные проверки внутри других обработчиков.

if __name__ == '__main__':
    bot.run()
