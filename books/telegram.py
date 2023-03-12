import os

import requests


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_USER_ID = os.environ["TELEGRAM_USER_ID"]


def send_telegram_message(text, telegram_account_id='TELEGRAM_USER_ID'):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    body = {
        "chat_id": telegram_account_id,
        "text": text,
    }
    requests.post(url, json=body)
