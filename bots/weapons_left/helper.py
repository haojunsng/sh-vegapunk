import json
import requests
import os

WEAPONS_LEFT_BOT_TOKEN = os.environ.get('WEAPONS_LEFT_BOT_TOKEN')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{WEAPONS_LEFT_BOT_TOKEN}"


def parse_split_message(message_text):
    
    # Format will be enforced by the bot - reject if not valid
    lines = message_text.strip().split('\n')
    
    # Start with /split
    if not lines or lines[0].strip() != '/split':
        return {'error': 'Message must start with /split'}
    
    # Must have at least two expense lines
    expense_lines = [line.strip() for line in lines[1:] if line.strip()]
    if len(expense_lines) < 2:
        return {'error': 'Nothing to split if there are less than 2 expenses.'}
    
    expenses = {}
    
    for i, line in enumerate(expense_lines, 2):
        parts = line.split()
        
        # Must have exactly 2 parts
        if len(parts) != 2:
            return {'error': f'Line {i}: "{line}" - Must be exactly "Name Amount" format'}
        
        name, amount_str = parts
        
        # Amount validation
        try:
            amount = float(amount_str)
            if amount < 0:
                return {'error': f'Line {i}: "{amount_str}" - Amount cannot be negative'}
        except ValueError:
            return {'error': f'Line {i}: "{amount_str}" - Must be a valid number'}
        
        # Check for duplicate names
        if name in expenses:
            return {'error': f'Line {i}: "{name}" - Name already exists'}
        
        expenses[name] = amount
    
    return expenses

def parse_webhook(event):
    """
    Parse the incoming webhook from Telegram.
    
    Args:
        event: API Gateway event
        
    Returns:
        dict: {'chat_id': int, 'message_text': str} or None if not a text message
    """
    try:
        # Parse the JSON body
        body = json.loads(event.get('body', '{}'))
        
        # Extract message data
        message = body.get('message', {})
        if not message:
            return None  # Not a message update
        
        chat_id = message.get('chat', {}).get('id')
        message_text = message.get('text')
        
        if not chat_id or not message_text:
            return None  # Missing required fields
        
        return {
            'chat_id': chat_id,
            'message_text': message_text
        }
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing webhook: {str(e)}")
        return None


def send_telegram_message(chat_id, text):
    """
    Send a message back to Telegram.
    
    Args:
        chat_id: Telegram chat ID
        text: Message text to send
    """
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Message sent successfully to chat {chat_id}")
        print(f"Text: {text}")

    except requests.RequestException as e:
        print(f"Error sending message: {str(e)}")
        raise


def create_response(status_code, body):
    """
    Create HTTP response for API Gateway.
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': body})
    }

def parse_split2_input(text):
    """
    Parse /split2 input in format:
    payer haojun
    share all 25
    share amos apple 15
    share haojun apple 10
    amos 23 1.9
    apple 20 5.8 1.9
    """
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    
    if len(lines) < 2:
        raise ValueError("Need at least payer and one expense line.")
    
    # Parse payer (first line)
    payer_line = lines[0].split()
    if len(payer_line) < 2:
        raise ValueError("Payer line must be: 'payer-name'.")
    payer = payer_line[1].lower()
    
    sharing_items = []
    individual_expenses = {}
    
    # Process remaining lines
    for line in lines[1:]:
        parts = line.split()

        # In case someone sends a blank line
        if not parts:
            continue
            
        # Check if this is a share line
        if parts[0].lower() == 'share':
            if len(parts) < 3:
                raise ValueError(f"Invalid share line: {line}.")
            
            # Parse sharing participants and amount
            if parts[1].lower() == 'all':
                # share all amount1 amount2 amount3...
                if len(parts) < 3:
                    raise ValueError(f"Invalid 'share all' line: {line}.")
                participants = ['all']
                # Sum all amounts after 'all'
                total_amount = sum(float(part.replace(',', '')) for part in parts[2:])
                amount = total_amount
            else:
                if len(parts) < 4:
                    raise ValueError(f"Invalid share line: {line}.")
                # share person1 person2 ... amount
                # Find the first number (amount)
                amount_index = 2
                for i in range(len(parts)):
                    if str(parts[i]).replace('.', '').isdigit():
                        amount_index = i
                        break

                if amount_index == 2:
                    raise ValueError(f"No amount found in share line: {line}.")
                
                participants = [p.lower() for p in parts[1:amount_index]]
                try:
                    amount = sum(float(part) for part in parts[amount_index:])
                except ValueError:
                    raise ValueError(f"Invalid amount in share item: {line}.")
            
            sharing_items.append({
                'participants': participants,
                'amount': amount
            })
            
        else:
            # Individual expense line
            name = parts[0].lower()
            expenses = sum(float(part) for part in parts[1:])
            if name in individual_expenses:
                individual_expenses[name] += expenses
            else:
                individual_expenses[name] = expenses
    
    return {
        'payer': payer,
        'sharing_items': sharing_items,
        'individual_expenses': individual_expenses
    }
