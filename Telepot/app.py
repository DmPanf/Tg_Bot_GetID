import os
import configparser
from datetime import datetime
import telepot
from telepot.loop import MessageLoop
from dotenv import load_dotenv

def load_config():
    """Load configuration from bot_config.ini and environment variables."""
    config = configparser.ConfigParser()
    if not os.path.exists('bot_config.ini'):
        raise FileNotFoundError("bot_config.ini not found!")
    config.read('bot_config.ini')
    
    try:
        log_file = config['LOGS']['path']
    except KeyError:
        log_file = "./logs/default_log.txt"  # default value if not found in config

    load_dotenv()
    TOKEN = os.environ.get("TG_TOKEN")
    if not TOKEN:
        raise ValueError("TG_TOKEN is not set in the environment variables or .env file!")

    return TOKEN, log_file

def log_message(msg, log_file):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    user_info = (f"▫️ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                 f"User ID: {msg['from']['id']} | "
                 f"Username: {msg['from'].get('username', 'N/A')} | "
                 f"First Name: {msg['from'].get('first_name', 'N/A')} | "
                 f"Last Name: {msg['from'].get('last_name', 'N/A')} | "
                 f"Language: {msg['from'].get('language_code', 'N/A')}")
    
    chat_info = (f"Chat Type: {chat_type} | Chat ID: {chat_id}")

    log_text = f"🔹{user_info} | Chat Info: [{chat_info}] | Message Text: {msg['text']}\n"

    with open(log_file, "a") as file:
        file.write(log_text)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text' and msg['text'] == '/start':
        user_id = msg['from']['id']
        response_text = (f"Hello, I'm Zero Bot =>\n"
                         f"👤 <b>user ID:</b> <code>{user_id}</code>\n"
                         f"👥 <b>chat ID:</b> <code>{chat_id}</code>")
        
        bot.sendMessage(chat_id, response_text, parse_mode='HTML')
        log_message(msg, LOG_PATH)

    elif 'forward_from' in msg:
        original_user_id = msg['forward_from']['id']
        response_text = (f"👤 <b>Original User ID (from forwarded message):</b> <code>{original_user_id}</code>\n"
                         f"👥 <b>Chat ID:</b> <code>{chat_id}</code>")
        
        bot.sendMessage(chat_id, response_text, parse_mode='HTML')
        log_message(msg, LOG_PATH)

TOKEN, LOG_PATH = load_config()
bot = telepot.Bot(TOKEN)

if __name__ == '__main__':
    MessageLoop(bot, handle).run_as_thread()
    print('Listening ...')

    import time
    while True:
        time.sleep(10)
