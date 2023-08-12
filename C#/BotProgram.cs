using System;
using Telegram.Bot;
using Telegram.Bot.Args;

namespace MyTelegramBot
{
    class Program
    {
        static ITelegramBotClient botClient;
        static string logPath = "./logs/default_log.txt"; // Простой путь для логов, замените, если нужно

        static void Main()
        {
            botClient = new TelegramBotClient("YOUR_TOKEN_HERE"); // Замените на ваш токен

            botClient.OnMessage += Bot_OnMessage;
            botClient.StartReceiving();

            Console.WriteLine("Bot is running...");
            Console.ReadLine(); // Держит приложение работающим
            botClient.StopReceiving();
        }

        static async void Bot_OnMessage(object sender, MessageEventArgs e)
        {
            if (e.Message.Text != null)
            {
                Console.WriteLine($"Received a message from {e.Message.Chat.Id}.");

                if (e.Message.Text == "/start")
                {
                    await botClient.SendTextMessageAsync(
                        chatId: e.Message.Chat.Id,
                        text: $"Hello, I'm Zero Bot =>\n👤 <b>user ID:</b> <code>{e.Message.From.Id}</code>\n👥 <b>chat ID:</b> <code>{e.Message.Chat.Id}</code>",
                        parseMode: Telegram.Bot.Types.Enums.ParseMode.Html
                    );
                }

                LogMessage(e.Message);
            }
        }

        static void LogMessage(Telegram.Bot.Types.Message message)
        {
            string user_info = $"{message.Date:yyyy-MM-dd HH:mm:ss} | " +
                               $"User ID: {message.From.Id} | " +
                               $"Username: {message.From.Username} | " +
                               $"First Name: {message.From.FirstName} | " +
                               $"Last Name: {message.From.LastName} | " +
                               $"Language: {message.From.LanguageCode}";

            string chat_info = $"Chat Type: {message.Chat.Type} | " +
                               $"Chat ID: {message.Chat.Id} | " +
                               $"Chat Title: {message.Chat.Title ?? "N/A"}";

            string log_text = $"🔹{user_info} | Chat Info: [{chat_info}] | Message Text: {message.Text}\n";

            System.IO.File.AppendAllText(logPath, log_text);
        }
    }
}
