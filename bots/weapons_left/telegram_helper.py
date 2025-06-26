from helper import parse_split_message
from split_bill import calculate_bill_split

def get_welcome_message():
    """Returns the welcome message for new users"""
    return """🤖 **Hello! I am Lilith, one of Vegapunk's satellites!** 💰

I'm here to help you split bills with your crew! Here's how to use me:

📝 **COMMAND FORMAT:** 📝
```
/split
[Name] [Amount Paid]
[Name] [Amount Paid]
...
```

🍖 **EXAMPLE:** 🍖
```
/split
Luffy 50
Zoro 30
Nami 0
Usopp 20
```

✨ **FEATURES:** ✨
• Automatically calculates who owes what
• Minimizes the number of transactions needed
• Shows optimal settlement plan
• Handles any number of people

🚀 **Ready to split?** Just send me `/split` followed by your expenses!""" 🚀

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
    balances = result['balances']
    
    response = "💰 **BILL SPLIT RESULTS** 💰\n\n"
    
    # Summary section
    response += "📊 **SUMMARY** 📊\n"
    response += f"┌ Total Bill: ${total:.2f}\n"
    response += f"├ Split Between: {len(balances)} people\n"
    response += f"└ Each Person Pays: ${per_person:.2f}\n\n"
    
    # Individual breakdown with emojis
    response += "👥 **INDIVIDUAL BREAKDOWN**\n"
    for person, balance in balances.items():
        if balance > 0.01:
            response += f"✅ {person}: +${balance:.2f}\n"
        elif balance < -0.01:
            response += f"❌ {person}: -${-balance:.2f}\n"
        else:
            response += f"⚖️ {person}: $0.00 (all settled)\n"
    
    # Settlement instructions with better formatting
    if settlements:
        response += f"\n🔄 **SETTLEMENT PLAN** ({len(settlements)} transactions) 🔄\n"
        
        for i, settlement in enumerate(settlements, 1):
            response += f"{i}. 💸 **{settlement['from']}** → **{settlement['to']}**: ${settlement['amount']:.2f} 💸\n"
        
    else:
        response += f"🎉 **EVERYONE IS ALREADY EVEN!** 🎉\n"

    # Add a fun footer
    response += f"\n---\n"
    response += f"🤖 Powered by Lilith 🤖"
    
    return response
