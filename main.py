import requests
from bs4 import BeautifulSoup
import html
import time
import logging
import signal
import sys
import os
from dotenv import load_dotenv


load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


URL = "https://tishreen.edu.sy/ar/Schedual/Results"
HEADERS = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
DATA = {
    "facultyId": 51,
    "departmentId": 56,
    "studyYearId": 11,
    "semesterId": 2,
}


new_array = []

def send_telegram_message(message):
    
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(telegram_url, data=payload)
        response.raise_for_status()
        logging.info("Message sent to Telegram successfully.")
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")

def fetch_and_parse_h3_elements():
    
    global new_array
    try:
        
        response = requests.post(URL, headers=HEADERS, data=DATA, timeout=25)
        response.raise_for_status()

        
        soup = BeautifulSoup(response.text, "html.parser")
        h3_elements = soup.find_all("h3")
        decoded_h3_texts = [html.unescape(h3.get_text()) for h3 in h3_elements]

        
        if not new_array:
            new_array = decoded_h3_texts[:]
            logging.info("The first array has been initialized with current elements.")
        else:
            difference = [item for item in decoded_h3_texts if item not in new_array]
            if difference:
                logging.info(f"New elements found: {difference}")
                send_telegram_message("\n".join(difference))  
                new_array = decoded_h3_texts[:]  
            else:
                logging.info("No new elements detected.")
    except Exception as e:
        logging.error(f"Error during request or parsing: {e}")
        time.sleep(5)  

def graceful_exit(signum, frame):
    
    logging.info("Shutting down gracefully...")
    sys.exit(0)


signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

if __name__ == "__main__":
    logging.info("The Telegram Bot Has Been Started!")
    while True:
        fetch_and_parse_h3_elements()
        time.sleep(10)  
