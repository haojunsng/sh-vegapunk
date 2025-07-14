import requests
import datetime
import json
import os

def lambda_handler(event, context):
    bot_token = os.environ["BOT_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    thread_id = os.environ["THREAD_ID"]
    
    today = datetime.date.today()
    next_monday = today + datetime.timedelta(days=(7 - today.weekday()))
    next_sunday = next_monday + datetime.timedelta(days=6)
    
    week_range = f"{next_monday.strftime('%b %d')} – {next_sunday.strftime('%b %d')}"

    question = f"🏃 TSRC Weekly Run Attendance ({week_range})"
    message_text = "Please select your availability for the upcoming week's runs."

    options = [
        "✅ Monday Evening",
        "✅ Wednesday Evening",
        "✅ Saturday Morning",
        "❌ None"
    ]

    url = f"https://api.telegram.org/bot{bot_token}/sendPoll"

    payload = {
        "chat_id": chat_id,
        "message_thread_id": thread_id,
        "question": question + "\n" + message_text,
        "options": json.dumps(options),
        "is_anonymous": False,
        "allows_multiple_answers": True
    }

    response = requests.post(url, data=payload)

    return {
        "statusCode": response.status_code,
        "body": response.json()
    }
