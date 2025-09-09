import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

FXRATESAPI_KEY = os.environ.get("FXRATESAPI_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def lambda_handler(event, context):
    # Build fxratesapi URL
    url = f"https://api.fxratesapi.com/latest?base=SGD&symbols=JPY&api_key={FXRATESAPI_KEY}"

    # Call fxratesapi
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    rate = data["rates"]["JPY"]

    now = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    message = f"⏰ Daily FX Update\n📅 {now}\n\n💵 1 SGD = {rate:.2f} JPY"

    # Send to Pythagoras Bot
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }).encode("utf-8")

    req = urllib.request.Request(telegram_url, data=payload)
    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode())
        print("Telegram response:", response_data)

    return {"statusCode": 200, "body": json.dumps(message)}
