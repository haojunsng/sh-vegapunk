from helper import parse_split_message
from split_bill import calculate_bill_split

def handle_telegram_message(message_text):

    expenses = parse_split_message(message_text)
    
    if 'error' in expenses:
        return f"{expenses['error']}\n\nFormat:\n/split\nLuffy 50\nZoro 30\nNami 0"
    

    result = calculate_bill_split(expenses)
    
    response = format_split_result(result)
    return response


def format_split_result(result):

    total = result['total']
    per_person = result['per_person']
    settlements = result['settlements']
    
    response = f"**Bill Split Results**\n"
    response += f"Total: ${total:.2f}\n"
    response += f"Per person: ${per_person:.2f}\n\n"
    
    response += "**Individual Status:**\n"
    for person, balance in result['balances'].items():
        if balance > 0.01:
            response += f"- {person}: should receive ${balance:.2f}\n"
        elif balance < -0.01:
            response += f"- {person}: owes ${-balance:.2f}\n"
        else:
            response += f"- {person}: even\n"
    
    # Settlement instructions
    if settlements:
        response += "\n**Who pays whom:**\n"
        for settlement in settlements:
            response += f"• {settlement['from']} pays {settlement['to']} ${settlement['amount']:.2f}\n"
    else:
        response += "\nEveryone is already even!"
    
    return response
