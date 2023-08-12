package main

import (
	"fmt"
	"gopkg.in/tucnak/telebot.v2"
	"io/ioutil"
	"log"
	"os"
	"time"
)

var LOG_PATH = "./logs/default_log.txt"

func logMessage(message *telebot.Message) {
	logDir := "./logs"
	if _, err := os.Stat(logDir); os.IsNotExist(err) {
		os.Mkdir(logDir, 0755)
	}

	currentTime := time.Now().Format("2006-01-02 15:04:05")
	userInfo := fmt.Sprintf("%s | User ID: %d | Username: %s | First Name: %s | Last Name: %s | Language: %s",
		currentTime, message.Sender.ID, message.Sender.Username, message.Sender.FirstName, message.Sender.LastName, message.Sender.LanguageCode)

	chatTitle := "N/A"
	if message.Chat.Title != "" {
		chatTitle = message.Chat.Title
	}
	chatInfo := fmt.Sprintf("Chat Type: %s | Chat ID: %d | Chat Title: %s", message.Chat.Type, message.Chat.ID, chatTitle)

	logText := fmt.Sprintf("🔹%s | Chat Info: [%s] | Message Text: %s\n", userInfo, chatInfo, message.Text)
	
	err := ioutil.WriteFile(LOG_PATH, []byte(logText), 0644)
	if err != nil {
		log.Fatalf("Failed writing to log file: %s", err)
	}
}

func main() {
	b, err := telebot.NewBot(telebot.Settings{
		Token: "YOUR_TELEGRAM_TOKEN_HERE",
		Poller: &telebot.LongPoller{Timeout: 10 * time.Second},
	})

	if err != nil {
		log.Fatalf("Failed to create new bot: %s", err)
		return
	}

	b.Handle("/start", func(m *telebot.Message) {
		response := fmt.Sprintf("Hello, I'm Zero Bot =>\n👤 <b>user ID:</b> <code>%d</code>\n👥 <b>chat ID:</b> <code>%d</code>", m.Sender.ID, m.Chat.ID)
		b.Send(m.Chat, response, telebot.ModeHTML)
		logMessage(m)
	})

	b.Handle(telebot.OnText, func(m *telebot.Message) {
		if m.IsForwarded() {
			response := fmt.Sprintf("👤 <b>Original User ID (from forwarded message):</b> <code>%d</code>\n👥 <b>Chat ID:</b> <code>%d</code>", m.OriginalSender.ID, m.Chat.ID)
			b.Send(m.Chat, response, telebot.ModeHTML)
			logMessage(m)
		}
	})

	b.Start()
}
