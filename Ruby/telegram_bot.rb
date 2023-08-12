require 'telegram/bot'

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

LOG_PATH = "./logs/default_log.txt"

Telegram::Bot::Client.run(TOKEN) do |bot|
  bot.listen do |message|
    case message.text
    when '/start'
      bot.api.send_message(chat_id: message.chat.id, text: "Hello, I'm Zero Bot =>\n👤 User ID: #{message.from.id}\n👥 Chat ID: #{message.chat.id}")
      log_message(message)
    else
      log_message(message)
    end
  end
end

def log_message(message)
  user_info = "#{message.date} | " +
              "User ID: #{message.from.id} | " +
              "Username: #{message.from.username} | " +
              "First Name: #{message.from.first_name} | " +
              "Last Name: #{message.from.last_name} | " +
              "Language: #{message.from.language_code}"

  chat_info = "Chat Type: #{message.chat.type} | " +
              "Chat ID: #{message.chat.id} | " +
              "Chat Title: #{message.chat.title || 'N/A'}"

  log_text = "🔹#{user_info} | Chat Info: [#{chat_info}] | Message Text: #{message.text}\n"
  
  File.open(LOG_PATH, 'a') { |file| file.write(log_text) }
end
