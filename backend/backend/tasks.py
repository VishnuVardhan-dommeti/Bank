from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Account, InterestTable, Transaction, Balance

# 🔹 Task 1: Calculate and Apply Interest for All Accounts
@shared_task
def calculate_interest():
    accounts = Account.objects.filter(status='Active')
    for account in accounts:
        try:
            interest_rate = InterestTable.objects.get(account_type=account.account_type).interest_rate
            interest_amount = (account.balance_amount * (interest_rate / 100))
            
            # Create a transaction entry for interest
            Transaction.objects.create(
                account=account,
                transaction_type='Interest',
                amount=interest_amount
            )

            # Update the account balance
            account.balance_amount += interest_amount
            account.save()

        except InterestTable.DoesNotExist:
            # Skip accounts with no interest rate set
            continue
    return "Interest calculation completed."

# 🔹 Task 2: Mark Dormant Accounts (No Activity for 6 Months)
@shared_task
def mark_dormant_accounts():
    six_months_ago = timezone.now() - timedelta(days=180)
    dormant_accounts = Account.objects.filter(last_transaction_date__lt=six_months_ago, status='Active')
    
    dormant_accounts.update(status='Dormant')
    return f"{dormant_accounts.count()} accounts marked as dormant."

# 🔹 Task 3: Enforce Overdraft Limits
@shared_task
def enforce_overdraft_limits():
    overdrawn_accounts = Account.objects.filter(balance_amount__lt=-1 * models.F('overdraft_limit'))
    
    for account in overdrawn_accounts:
        account.status = 'Closed'
        account.save()

    return f"{overdrawn_accounts.count()} accounts closed due to overdraft violation."

# 🔹 Task 4: Generate Monthly Account Summaries
@shared_task
def generate_monthly_summaries():
    accounts = Account.objects.filter(status='Active')
    summary_data = []

    for account in accounts:
        transactions = Transaction.objects.filter(account=account, timestamp__month=timezone.now().month)
        total_credits = sum(t.amount for t in transactions if t.transaction_type in ['Deposit', 'Transfer In'])
        total_debits = sum(t.amount for t in transactions if t.transaction_type in ['Withdraw', 'Transfer Out'])
        
        summary_data.append({
            "Account Number": account.account_number,
            "Total Deposits": total_credits,
            "Total Withdrawals": total_debits,
            "Net Change": total_credits - total_debits,
        })

    # Save or send report (e.g., via email, file, etc.)
    return summary_data

# 🔹 Task 5: Save Session Data Periodically
@shared_task
def save_session_data(session_key, data):
    from django.contrib.sessions.models import Session
    session, _ = Session.objects.get_or_create(session_key=session_key)
    session_data = session.get_decoded()
    session_data.update(data)
    session.session_data = session.encode(session_data)
    session.save()

    return f"Session data for {session_key} saved successfully."

# 🔹 Task 6: Load Session Data
@shared_task
def load_session_data(session_key):
    from django.contrib.sessions.models import Session
    try:
        session = Session.objects.get(session_key=session_key)
        return session.get_decoded()
    except Session.DoesNotExist:
        return {}
