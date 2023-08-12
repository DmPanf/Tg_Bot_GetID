#!/bin/bash

TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
URL="https://api.telegram.org/bot$TOKEN"

check_updates() {
    local offset="$1"
    curl -s "$URL/getUpdates?offset=$offset" | jq -r '.result[] | .message.text, .message.chat.id, .update_id'
}

send_message() {
    local chat_id="$1"
    local text="$2"
    curl -s -X POST "$URL/sendMessage" -d chat_id="$chat_id" -d text="$text" > /dev/null
}

OFFSET=0

while true; do
    UPDATES=$(check_updates "$OFFSET")
    set -- $UPDATES

    while [ $# -gt 0 ]; do
        MESSAGE_TEXT=$1
        CHAT_ID=$2
        UPDATE_ID=$3

        if [[ $MESSAGE_TEXT == "/start" ]]; then
            send_message "$CHAT_ID" "Hello, I'm Zero Bot. 👋"
        fi

        let "OFFSET=UPDATE_ID+1"

        shift 3
    done

    sleep 10
done
