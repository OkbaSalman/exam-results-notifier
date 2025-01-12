import requests
import os
from dotenv import load_dotenv


load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

MESSAGE = "Test message from the bot!"


url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
response = requests.post(url, data={"chat_id": TELEGRAM_CHANNEL_ID, "text": MESSAGE})


if response.status_code == 200:
    print("Message sent successfully!")
else:
    print(f"Failed to send message. Response: {response.json()}")
