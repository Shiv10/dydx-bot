import requests
from decouple import config

# Send Message
def send_message(message):
    bot_token = config("TELEGRAM_TOKEN")
    chat_id = config("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": 0
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return "sent"
    else:
        return "failed"