import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;

import java.io.*;
import java.nio.file.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;

public class MyTelegramBot extends TelegramLongPollingBot {
    private String TOKEN;
    private String LOG_PATH;

    public MyTelegramBot() {
        loadConfig();
    }

    private void loadConfig() {
        Properties prop = new Properties();
        InputStream input = null;

        try {
            input = new FileInputStream("bot_config.ini");
            prop.load(input);

            LOG_PATH = prop.getProperty("LOGS.path", "./logs/default_log.txt");
            TOKEN = System.getenv("TG_TOKEN");

            if (TOKEN == null) {
                throw new RuntimeException("TG_TOKEN is not set in the environment variables!");
            }

        } catch (IOException ex) {
            ex.printStackTrace();
        } finally {
            if (input != null) {
                try {
                    input.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private void logMessage(Message message) {
        try {
            String current_time = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());

            String user_info = String.format("%s | User ID: %s | Username: %s | First Name: %s | Last Name: %s | Language: %s",
                    current_time, message.getFrom().getId(), message.getFrom().getUserName(),
                    message.getFrom().getFirstName(), message.getFrom().getLastName(), message.getFrom().getLanguageCode());

            String chat_info = String.format("Chat Type: %s | Chat ID: %s | Chat Title: %s",
                    message.getChat().getType(), message.getChat().getId(), message.getChat().getTitle());

            String log_text = String.format("🔹%s | Chat Info: [%s] | Message Text: %s\n", user_info, chat_info, message.getText());

            Files.write(Paths.get(LOG_PATH), log_text.getBytes(), StandardOpenOption.APPEND, StandardOpenOption.CREATE);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onUpdateReceived(Update update) {
        if (update.hasMessage()) {
            Message message = update.getMessage();

            if (message.isCommand() && "/start".equals(message.getText())) {
                sendReply(message, String.format("Hello, I'm Zero Bot =>\n👤 <b>user ID:</b> <code>%s</code>\n👥 <b>chat ID:</b> <code>%s</code>",
                        message.getFrom().getId(), message.getChat().getId()));
                logMessage(message);
            } else if (message.getForwardFrom() != null) {
                sendReply(message, String.format("👤 <b>Original User ID (from forwarded message):</b> <code>%s</code>\n👥 <b>Chat ID:</b> <code>%s</code>",
                        message.getForwardFrom().getId(), message.getChat().getId()));
                logMessage(message);
            }
        }
    }

    private void sendReply(Message receivedMessage, String text) {
        SendMessage message = new SendMessage()
                .setChatId(receivedMessage.getChatId())
                .setText(text)
                .setParseMode("HTML");

        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    @Override
    public String getBotUsername() {
        return "YOUR_BOT_USERNAME";
    }

    @Override
    public String getBotToken() {
        return TOKEN;
    }

    public static void main(String[] args) {
        try {
            TelegramBotsApi botsApi = new TelegramBotsApi(DefaultBotSession.class);
            botsApi.registerBot(new MyTelegramBot());
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }
}
