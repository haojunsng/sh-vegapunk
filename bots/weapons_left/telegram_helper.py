from helper import parse_split_message, parse_split2_input
from split_bill import calculate_bill_split, calculate_split2

def get_welcome_message():
    """Returns the welcome message for new users"""
    return """🤖 *Hello! I am Lilith, one of Vegapunk's satellites!* 💰

I'm here to help you split bills with your crew! Here's how to use me:

🍖 *EXAMPLES:* 🍖

_Equal Split_
- Best for when you're just splitting the bill equally with people who paid different amounts - Chomp Chomp / Newton Circus / Bedok85.
```
/split
Luffy 50
Zoro 30
Nami 0
Usopp 20
```

_Advanced Split_
- Best when your party had individual expenses and shared expenses.
- Add "no surcharges" at the end if expenses are already nett.
```
/split2
payer Luffy
share all 25 15 10
share Zoro Nami 30
share Nami Usopp 20
Zoro 23 1.9
Name 20 5.8 1.9
Usopp 10
no surcharges
```

✨ _FEATURES:_ ✨\n
• Automatically calculates who owes what.
• Minimizes the number of transactions needed
• Handles any number of people
• GST + Service Charge calculations (Singapore)


🚀 *Ready to split?* Just send me `/split` or `/split2` followed by your expenses!"""

def handle_telegram_message(message_text):
    
    if message_text.startswith('/split2'):
        # Handle advanced split
        try:
            # Check for no surcharges flag
            no_surcharges = 'no surcharges' in message_text.lower()
            clean_text = message_text.replace('/split2', '').replace('no surcharges', '').strip()
            
            data = parse_split2_input(clean_text)
            result = calculate_split2(data, no_surcharges=no_surcharges)
            response = format_split2_result(result)
            return response
            
        except ValueError as e:
            return f"❌ Error: {str(e)}\n\nPlease refer to the examples above for the correct format."
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}\n\nPlease check your input format."
    else:
        
        # Handle regular split
        try:
            expenses = parse_split_message(message_text)
        except ValueError as e:
            return f"❌ Error: {str(e)}\n\nPlease refer to the examples above for the correct format."
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}\n\nPlease check your input format."
        
        result = calculate_bill_split(expenses)
        response = format_split_result(result)
        return response


def format_split_result(result):
    total = result['total']
    per_person = result['per_person']
    settlements = result['settlements']
    balances = result['balances']
    
    response = "💰 *BILL SPLIT RESULTS* 💰\n\n"
    
    # Summary section
    response += "📊 *SUMMARY* 📊\n"
    response += f"┌ Total Bill: ${total:.2f}\n"
    response += f"├ Split Between: {len(balances)} people\n"
    response += f"└ Each Person Pays: ${per_person:.2f}\n\n"
    
    # Quick settlement summary
    if settlements:
        response += "🔄 *SETTLEMENT PLAN* ({len(settlements)} transactions) 🔄\n"
        for i, settlement in enumerate(settlements, 1):
            response += f"{i}. 💸 *{settlement['from']}* → *{settlement['to']}*: ${settlement['amount']:.2f} 💸\n"
    else:
        response += "🎉 *EVERYONE IS ALREADY EVEN!* 🎉\n"
    
    response += "\n📋 *DETAILED BREAKDOWN* (tap to expand)\n"
    response += "<blockquote expandable>"
    
    # Individual breakdown with emojis
    response += "👥 *INDIVIDUAL BREAKDOWN* 👥\n"
    for person, balance in balances.items():
        if balance > 0.01:
            response += f"✅ {person} - gets back ${balance:.2f}.\n"
        elif balance < -0.01:
            response += f"❌ {person} - needs to pay ${-balance:.2f}.\n"
        else:
            response += f"⚖️ {person} is even.\n"
    
    # Add a fun footer
    response += f"\n---\n"
    response += f"🤖 Powered by Lilith 🤖"
    response += "</blockquote>"
    
    return response

def format_split2_result(result):
    """
    Format the split2 calculation result for display.
    """
    payer = result['payer']
    sharing_items = result['sharing_items']
    individual_expenses = result['individual_expenses']
    breakdown = result['breakdown']
    no_surcharges = result['no_surcharges']

    response = ""
    response += "💰 *Advanced Bill Split Results* 💰\n\n"
    response += f"💳 *Paid by:* {payer} 💳\n\n"

    # Quick summary of what each person owes
    response += "💸 *QUICK SUMMARY* 💸\n"
    for name, details in breakdown.items():
        response += f"• *{name}* owes *${details['total']:.2f}* to {payer}\n"
    
    response += "\n📋 *DETAILED BREAKDOWN* (tap to expand)\n"
    response += "<blockquote expandable>"

    # Sharing items
    if sharing_items:
        response += "🍽️ *Shared Items:* 🍽️\n"
        for item in sharing_items:
            participants = item['participants']
            amount = item['amount']
            if participants == ['all']:
                response += f"  • Everyone (including {payer}): ${amount:.2f}\n"
            else:
                response += f"  • {', '.join(participants)}: ${amount:.2f}\n"
        response += "\n"

    # Individual expenses
    if individual_expenses:
        response += "👤 *Individual Expenses:* 👤\n"
        for name, amount in individual_expenses.items():
            response += f"  • {name}: ${amount:.2f}\n"
        response += "\n"

    # What each person owes
    response += "💸 *What Each Person Owes:* 💸\n"
    for name, details in breakdown.items():
        response += "\n"
        response += f"👤 *{name}:* 👤\n"
        if details['individual'] > 0:
            response += f"  Individual: ${details['individual']:.2f}\n"
        if details['sharing'] > 0:
            response += f"  Shared: ${details['sharing']:.2f}\n"
        response += f"  Subtotal: ${details['subtotal']:.2f}\n"
        if not no_surcharges:
            response += f"  Service Charge: ${details['service_charge']:.2f}\n"
            response += f"  GST: ${details['gst']:.2f}\n"
        response += f"  *Total: ${details['total']:.2f}*\n"

        response += f"{name} owes ${details['total']:.2f} to {payer}. \n"

    response += "\n---\n"
    response += f"🤖 Powered by Lilith 🤖"
    response += "</blockquote>"
    
    return response
