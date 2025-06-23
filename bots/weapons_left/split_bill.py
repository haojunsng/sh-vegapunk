def calculate_bill_split(expenses):
    
    # Calculate totals
    total_amount = sum(expenses.values())
    num_people = len(expenses)
    per_person = round(total_amount / num_people, 2)

    balances = {}
    for person, paid in expenses.items():
        balances[person] = round(paid - per_person, 2)
    
    # Generate settlements
    settlements = calculate_settlements(balances)
    
    return {
        'total': total_amount,
        'per_person': per_person,
        'balances': balances,
        'settlements': settlements
    }


def calculate_settlements(balances):

    creditors = [(person, amount) for person, amount in balances.items() if amount > 0]
    debtors = [(person, -amount) for person, amount in balances.items() if amount < 0]
    
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)
    
    settlements = []
    
    # Loop until all balances are zero - SETTLED
    while creditors and debtors:
        creditor_name, credit_amount = creditors[0]
        debtor_name, debt_amount = debtors[0]
        
        # Settle the smaller of the two amounts
        settlement_amount = min(credit_amount, debt_amount)
        
        settlements.append({
            'from': debtor_name,
            'to': creditor_name,
            'amount': round(settlement_amount, 2)
        })

        new_credit = credit_amount - settlement_amount
        new_debt = debt_amount - settlement_amount

        if new_credit == 0:
            creditors.pop(0)
        else:
            creditors[0] = (creditor_name, new_credit)
            
        if new_debt == 0:
            debtors.pop(0)
        else:
            debtors[0] = (debtor_name, new_debt)
    
    return settlements
