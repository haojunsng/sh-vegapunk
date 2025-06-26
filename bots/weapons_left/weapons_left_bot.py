from helper import parse_webhook, send_telegram_message, create_response
from telegram_helper import handle_telegram_message, get_welcome_message

def lambda_handler(event, context):

    try:
        # Parse the webhook payload
        webhook_data = parse_webhook(event)
        if not webhook_data:
            return create_response(200, "OK")  # Ignore non-message updates
        
        chat_id = webhook_data['chat_id']
        message_text = webhook_data['message_text']
        
        # Process the message with our bot logic
        if message_text.startswith('/split'):
            bot_response = handle_telegram_message(message_text)
        else:
            bot_response = get_welcome_message()
        
        # Send response back to Telegram
        send_telegram_message(chat_id, bot_response)
        
        return create_response(200, "OK")
        
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return create_response(500, f"Error: {str(e)}")
