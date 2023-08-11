import org.telegram.telegrambots.bots.TelegramLongPollingBot
import org.telegram.telegrambots.meta.TelegramBotsApi
import org.telegram.telegrambots.meta.api.methods.send.SendMessage
import org.telegram.telegrambots.meta.api.objects.Message
import org.telegram.telegrambots.meta.api.objects.Update
import org.telegram.telegrambots.meta.exceptions.TelegramApiException
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession
import java.io.FileInputStream
import java.nio.file.Files
import java.nio.file.Paths
import java.nio.file.StandardOpenOption
import java.text.SimpleDateFormat
import java.util.*

class MyTelegramBot : TelegramLongPollingBot() {
    private lateinit var TOKEN: String
    private var LOG_PATH = "./logs/default_log.txt"

    init {
        loadConfig()
    }

    private fun loadConfig() {
        val prop = Properties()

        FileInputStream("bot_config.ini").use { input ->
            prop.load(input)
            LOG_PATH = prop.getProperty("LOGS.path", "./logs/default_log.txt")
            TOKEN = System.getenv("TG_TOKEN") ?: throw RuntimeException("TG_TOKEN is not set in the environment variables!")
        }
    }

    private fun logMessage(message: Message) {
        val current_time = SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(Date())

        val user_info = String.format(
            "%s | User ID: %s | Username: %s | First Name: %s | Last Name: %s | Language: %s",
            current_time, message.from.id, message.from.userName,
            message.from.firstName, message.from.lastName, message.from.languageCode
        )

        val chat_info = String.format(
            "Chat Type: %s | Chat ID: %s | Chat Title: %s",
            message.chat.type, message.chat.id, message.chat.title
        )

        val log_text = "🔹$user_info | Chat Info: [$chat_info] | Message Text: ${message.text}\n"

        Files.write(Paths.get(LOG_PATH), log_text.toByteArray(), StandardOpenOption.APPEND, StandardOpenOption.CREATE)
    }

    override fun onUpdateReceived(update: Update) {
        update.message?.let { message ->
            when {
                message.isCommand && "/start" == message.text -> {
                    sendReply(
                        message, "Hello, I'm Zero Bot =>\n👤 <b>user ID:</b> <code>${message.from.id}</code>\n👥 <b>chat ID:</b> <code>${message.chat.id}</code>"
                    )
                    logMessage(message)
                }
                message.forwardFrom != null -> {
                    sendReply(
                        message, "👤 <b>Original User ID (from forwarded message):</b> <code>${message.forwardFrom.id}</code>\n👥 <b>Chat ID:</b> <code>${message.chat.id}</code>"
                    )
                    logMessage(message)
                }
            }
        }
    }

    private fun sendReply(receivedMessage: Message, text: String) {
        val message = SendMessage()
            .setChatId(receivedMessage.chatId)
            .setText(text)
            .setParseMode("HTML")

        try {
            execute(message)
        } catch (e: TelegramApiException) {
            e.printStackTrace()
        }
    }

    override fun getBotUsername() = "YOUR_BOT_USERNAME"

    override fun getBotToken() = TOKEN

    companion object {
        @JvmStatic
        fun main(args: Array<String>) {
            try {
                val botsApi = TelegramBotsApi(DefaultBotSession::class.java)
                botsApi.registerBot(MyTelegramBot())
            } catch (e: TelegramApiException) {
                e.printStackTrace()
            }
        }
    }
}
