library(telegram.bot)

# Установите ваш токен бота
token <- 'YOUR_TELEGRAM_BOT_TOKEN'

# Создайте объект бота
bot <- Bot(token = token)

# Функция приветствия для команды /start
startHandler <- function(bot, update) {
  text <- sprintf("Hello, I'm Zero Bot. 👋")
  sendMessage(bot, chat_id = update$message$chat_id, text = text)
}

# Добавьте команду /start
add_handler(bot, command = 'start', callback = startHandler)

# Запустите бота
while(TRUE) {
  updates <- getUpdates(bot)
  if (length(updates$result) > 0) {
    handle_update(bot, updates$result)
    bot$offset <- updates$result[[length(updates$result)]]$update_id + 1
  }
  Sys.sleep(1)
}
