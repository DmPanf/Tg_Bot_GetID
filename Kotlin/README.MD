# Kotlin Telegram Bot based on TelegramBots

## Установка и настройка в Manjaro Linux & Ubuntu Linux

### Manjaro Linux:

- **`sudo pacman -S jdk-openjdk`**
- **`sudo pacman -S kotlin`**
- **`kotlinc MyTelegramBot.kt -include-runtime -d MyTelegramBot.jar`**
- **`java -jar MyTelegramBot.jar`**
- Можно использовать системы управления зависимостями TelegramBots в проек, такие как Maven или Gradle, чтобы автоматически обрабатывать эти зависимости.

### Ubuntu Linux:

- **`sudo apt update`**
- **`sudo apt install openjdk-11-jdk`**
- **`sudo snap install --classic kotlin`**
- **`kotlinc MyTelegramBot.kt -include-runtime -d MyTelegramBot.jar`**
- **`java -jar MyTelegramBot.jar`**
- Можно использовать системы управления зависимостями TelegramBots в проек, такие как Maven или Gradle, чтобы автоматически обрабатывать эти зависимости.
