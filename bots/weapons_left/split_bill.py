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

def calculate_split2(data, gst_rate=0.09, service_charge_rate=0.10, no_surcharges=False):

    payer = data['payer']
    sharing_items = data['sharing_items']
    individual_expenses = data['individual_expenses']
    
    # Get all participants (excluding payer)
    all_participants = set(individual_expenses)
    for item in sharing_items:
        if item['participants'] == ['all']:
            continue
        all_participants.update(item['participants'])
    all_participants.discard(payer)
    
    if not all_participants:
        raise ValueError("No participants found")
    
    # Calculate sharing per person for each item
    sharing_breakdown = {}
    for item in sharing_items:
        participants = item['participants']
        amount = item['amount']
        
        if participants == ['all']:
            # Everyone shares equally - including payer that's why +1
            share_per_person = amount / (len(all_participants) + 1)
            for participant in all_participants:
                if participant not in sharing_breakdown:
                    sharing_breakdown[participant] = 0
                sharing_breakdown[participant] += share_per_person
        else:
            # Specific people share
            share_per_person = amount / len(participants)
            for participant in participants:
                if participant not in sharing_breakdown:
                    sharing_breakdown[participant] = 0
                sharing_breakdown[participant] += share_per_person
    
    # Calculate what each person owes
    breakdown = {}
    for name in all_participants:
        individual_share = individual_expenses.get(name, 0)
        sharing_share = sharing_breakdown.get(name, 0)
        subtotal_share = individual_share + sharing_share
        
        if no_surcharges:
            total_share = subtotal_share
        else:
            # Calculate surcharges: Service Charge first, then GST on subtotal + service charge
            service_charge_share = subtotal_share * service_charge_rate
            gst_share = (subtotal_share + service_charge_share) * gst_rate
            total_share = subtotal_share + service_charge_share + gst_share
        
        breakdown[name] = {
            'individual': individual_share,
            'sharing': sharing_share,
            'subtotal': subtotal_share,
            'gst': gst_share if not no_surcharges else 0,
            'service_charge': service_charge_share if not no_surcharges else 0,
            'total': total_share
        }
    
    return {
        'payer': payer,
        'sharing_items': sharing_items,
        'individual_expenses': individual_expenses,
        'breakdown': breakdown,
        'no_surcharges': no_surcharges
    }
