import { Telegraf } from 'telegraf';

const TOKEN = "YOUR_TELEGRAM_BOT_TOKEN";
const LOG_PATH = "./logs/default_log.txt";

const bot = new Telegraf(TOKEN);

const logMessage = (ctx: any) => {
    const message = ctx.message;
    const user_info = `${new Date(message.date * 1000).toISOString()} | User ID: ${message.from.id} | Username: ${message.from.username} | First Name: ${message.from.first_name} | Last Name: ${message.from.last_name} | Language: ${message.from.language_code}`;
    const chat_info = `Chat Type: ${message.chat.type} | Chat ID: ${message.chat.id} | Chat Title: ${message.chat.title || 'N/A'}`;
    const log_text = `🔹${user_info} | Chat Info: [${chat_info}] | Message Text: ${message.text}\n`;

    require('fs').appendFileSync(LOG_PATH, log_text);
}

bot.start((ctx) => {
    ctx.reply(`Hello, I'm Zero Bot =>\n👤 User ID: ${ctx.message?.from.id}\n👥 Chat ID: ${ctx.message?.chat.id}`);
    logMessage(ctx);
});

bot.on('message', (ctx) => logMessage(ctx));

bot.launch();
