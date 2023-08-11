# потребуется api_id и api_hash, которые можно получить на my.telegram.org
import os
import configparser
from datetime import datetime
from telethon import TelegramClient, events
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
        log_file = "./logs/default_log.txt"

    load_dotenv()
    TOKEN = os.environ.get("TG_TOKEN")
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")

    if not TOKEN or not API_ID or not API_HASH:
        raise ValueError("TG_TOKEN, API_ID, or API_HASH is missing!")

    return TOKEN, log_file, API_ID, API_HASH

def log_message(event, log_file):
    user = event.sender
    chat = event.chat

    user_info = (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                 f"User ID: {user.id} | "
                 f"Username: {user.username or 'N/A'} | "
                 f"First Name: {user.first_name or 'N/A'} | "
                 f"Last Name: {user.last_name or 'N/A'}")

    chat_info = (f"Chat Type: {'Group' if chat.megagroup else 'Private'} | "
                 f"Chat ID: {chat.id}")

    log_text = f"🔹{user_info} | Chat Info: [{chat_info}] | Message Text: {event.raw_text}\n"

    with open(log_file, "a") as file:
        file.write(log_text)

TOKEN, LOG_PATH, API_ID, API_HASH = load_config()

# Use the token to create a new bot session (bot token must be in the format of number:hash)
bot = TelegramClient('anon', API_ID, API_HASH).start(bot_token=TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user_id = event.sender_id
    chat_id = event.chat_id

    response_text = (f"Hello, I'm Zero Bot =>\n"
                     f"👤 <b>user ID:</b> <code>{user_id}</code>\n"
                     f"👥 <b>chat ID:</b> <code>{chat_id}</code>")
    
    await event.respond(response_text, parse_mode='html')
    log_message(event, LOG_PATH)

@bot.on(events.NewMessage())
async def message_handler(event):
    if event.forward:
        original_user_id = event.forward.sender_id
        chat_id = event.chat_id

        response_text = (f"👤 <b>Original User ID (from forwarded message):</b> <code>{original_user_id}</code>\n"
                         f"👥 <b>chat ID:</b> <code>{chat_id}</code>")
        
        await event.respond(response_text, parse_mode='html')
        log_message(event, LOG_PATH)

if __name__ == '__main__':
    print("Bot is running...")
    bot.run_until_disconnected()
