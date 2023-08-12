<?php

require 'vendor/autoload.php';

use Longman\TelegramBot\Telegram;
use Longman\TelegramBot\Request;

$API_KEY = 'YOUR_TELEGRAM_BOT_TOKEN';
$BOT_NAME = 'YOUR_BOT_NAME';

try {
    $telegram = new Telegram($API_KEY, $BOT_NAME);

    // Обработчик команды /start
    $telegram->on(function ($action) {
        $update = $action->getUpdate();
        $message = $update->getMessage();
        $chat_id = $message->getChat()->getId();

        return Request::sendMessage([
            'chat_id' => $chat_id,
            'text'    => "Hello, I'm Zero Bot. 👋",
        ]);
    }, function ($message) {
        return true; // Какой-либо условный обработчик, возвращающий true или false
    });

    $telegram->handle();

} catch (Exception $e) {
    // Здесь можно обработать исключения
    echo $e->getMessage();
}
