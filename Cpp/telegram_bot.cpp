#include <iostream>
#include <tgbot/tgbot.h>

int main() {
    TgBot::Bot bot("YOUR_TELEGRAM_BOT_TOKEN");

    bot.getEvents().onCommand("start", [&bot](TgBot::Message::Ptr message) {
        bot.getApi().sendMessage(message->chat->id, "Hello, I'm Zero Bot. 👋");
    });

    bot.getEvents().onAnyMessage([&bot](TgBot::Message::Ptr message) {
        printf("User wrote %s\n", message->text.c_str());
        if (StringTools::startsWith(message->text, "/start")) {
            return;
        }

        bot.getApi().sendMessage(message->chat->id, "Your message is: " + message->text);
    });

    try {
        printf("Bot username: %s\n", bot.getApi().getMe()->username.c_str());
        bot.getApi().deleteWebhook();
        TgBot::TgLongPoll longPoll(bot);
        while (true) {
            printf("Long poll started\n");
            longPoll.start();
        }
    } catch (TgBot::TgException& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
