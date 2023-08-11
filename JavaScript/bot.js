const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');
const { format } = require('date-fns');

dotenv.config();

const TOKEN = process.env.TG_TOKEN;
if (!TOKEN) {
    throw new Error("TG_TOKEN is not set in the environment variables or .env file!");
}

const bot = new TelegramBot(TOKEN, {polling: true});

const LOG_PATH = './logs/default_log.txt';

function logMessage(message) {
    const log_dir = path.dirname(LOG_PATH);
    if (!fs.existsSync(log_dir)) {
        fs.mkdirSync(log_dir, { recursive: true });
    }
    
    const current_time = format(new Date(), 'yyyy-MM-dd HH:mm:ss');
    const user_info = `${current_time} | User ID: ${message.from.id} | Username: ${message.from.username} | First Name: ${message.from.first_name} | Last Name: ${message.from.last_name || 'N/A'} | Language: ${message.from.language_code}`;
    const chat_info = `Chat Type: ${message.chat.type} | Chat ID: ${message.chat.id} | Chat Title: ${message.chat.title || 'N/A'}`;
    const log_text = `🔹${user_info} | Chat Info: [${chat_info}] | Message Text: ${message.text}\n`;
    
    fs.appendFileSync(LOG_PATH, log_text);
}

bot.onText(/\/start/, (message) => {
    const response = `Hello, I'm Zero Bot =>\n👤 <b>user ID:</b> <code>${message.from.id}</code>\n👥 <b>chat ID:</b> <code>${message.chat.id}</code>`;
    bot.sendMessage(message.chat.id, response, {parse_mode: "HTML"});
    logMessage(message);
});

bot.on('message', (message) => {
    if (message.forward_from) {
        const response = `👤 <b>Original User ID (from forwarded message):</b> <code>${message.forward_from.id}</code>\n👥 <b>Chat ID:</b> <code>${message.chat.id}</code>`;
        bot.sendMessage(message.chat.id, response, {parse_mode: "HTML"});
        logMessage(message);
    }
});
