local telegram = require("telegram")

local TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
local LOG_PATH = "./logs/default_log.txt"

local bot = telegram(TOKEN)

local function log_message(message)
    local user_info = string.format("%s | User ID: %d | Username: %s | First Name: %s | Last Name: %s | Language: %s",
        os.date('%Y-%m-%d %H:%M:%S', message.date),
        message.from.id,
        message.from.username or 'N/A',
        message.from.first_name or 'N/A',
        message.from.last_name or 'N/A',
        message.from.language_code or 'N/A'
    )

    local chat_info = string.format("Chat Type: %s | Chat ID: %d | Chat Title: %s",
        message.chat.type,
        message.chat.id,
        message.chat.title or 'N/A'
    )

    local log_text = string.format("🔹%s | Chat Info: [%s] | Message Text: %s\n", user_info, chat_info, message.text or 'N/A')

    local file = io.open(LOG_PATH, "a")
    file:write(log_text)
    file:close()
end

bot.run(function(update)
    if update.message then
        local message = update.message
        if message.text == "/start" then
            local reply = string.format("Hello, I'm Zero Bot =>\n👤 User ID: %d\n👥 Chat ID: %d", message.from.id, message.chat.id)
            bot.sendMessage{chat_id=message.chat.id, text=reply}
        end
        log_message(message)
    end
end)
