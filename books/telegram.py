import os

import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_USER_ID = os.environ["TELEGRAM_USER_ID"]


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    body = {
        "chat_id": TELEGRAM_USER_ID,
        "text": text,
    }
    response = requests.post(url, json=body)
    print(response.text)
    response.raise_for_status()

