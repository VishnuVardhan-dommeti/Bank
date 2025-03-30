from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db import transaction


from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render

def custom_admin_login(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in. Please logout to go to the Website Home Page.")
        return redirect(request.META.get("HTTP_REFERER", "custom_admin_dashboard"))  # Stay on the same page
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("custom_admin_dashboard")
        else:
            messages.error(request, "Invalid credentials or not a superuser.")

    return render(request, "custom_admin/login.html")


def custom_admin_logout(request):
    logout(request)
    request.session.flush()  # Clears session data
    messages.success(request, "You have been logged out successfully.")
    return redirect("custom_admin_login")





@login_required
def custom_admin_dashboard(request):
    total_accounts = Account.objects.count()
    total_balance = Account.objects.aggregate(total_balance=models.Sum('balance'))['total_balance'] or 0.0

    recent_transactions = Transaction.objects.select_related('account').order_by('-timestamp')[:5]

    return render(request, "custom_admin/dashboard.html", {
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "recent_transactions": recent_transactions
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from django.contrib.auth.models import User
from django.db import transaction

def new_account(request):
    success = False  # Flag to indicate successful submission

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        balance = float(request.POST.get('balance'))
        account_type = request.POST.get('account_type')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use!")
            return redirect('new_account')

        try:
            user = User.objects.create_user(username=email, email=email, first_name=firstname, last_name=lastname, password=password)

            with transaction.atomic():
                account = Account.objects.create(
                    user=user,
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    password=password,
                    balance=balance,
                    account_type=account_type
                )
                messages.success(request, f"Account {account.account_number} created successfully!")
                success = True  # Set success flag to True
                return redirect(f"{request.path}?success=1")  # Redirect with success flag

        except Exception as e:
            messages.error(request, f"Error creating account: {e}")

    return render(request, 'custom_admin/new_account.html', {"success": success})


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Account  # Adjust based on your actual model import
from django.contrib.auth.hashers import make_password


def manage_account(request):
    accounts = Account.objects.all()
    return render(request, 'custom_admin/manage_account.html', {'accounts': accounts})

def delete_account(request, account_id):
    if request.method == "POST":
        account = get_object_or_404(Account, id=account_id)
        account.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

def edit_account(request, account_id):
    success = False  # Flag to indicate successful submission

    account = get_object_or_404(Account, id=account_id)
    print(f"Account ID: {account.firstname} {account.lastname}")
    

    if request.method == "POST":
        print("POST request received")

        if request.POST.get("firstname"):
            account.firstname = request.POST.get("firstname")
        if request.POST.get("lastname"):
            account.lastname = request.POST.get("lastname")
        if request.POST.get("email"):    
            account.email = request.POST.get("email")
        if request.POST.get("password"):
            account.password = make_password(request.POST.get("password"))  # Hash password

        account.save()
        print(f"Account ID: {account.firstname} {account.lastname}")

        messages.success(request, f"Account {account.account_number} updated successfully!")
        success = True  
        return redirect(f"{request.path}?success=1")

    return render(request, "custom_admin/edit_account.html", {"account": account, "success": success})



def transactions_view(request):
    transactions = Transaction.objects.select_related('account').order_by('-timestamp')
    return render(request, 'custom_admin/transactions.html', {'transactions': transactions})



from django.http import JsonResponse
from django.shortcuts import render
from .models import Account, Transaction  # Ensure Transaction model is imported

def deposit_view(request):
    if request.method == "GET":
        account_number = request.GET.get("account_number")
        if account_number:
            try:
                account = Account.objects.get(account_number=account_number)
                return JsonResponse({
                    "status": "success",
                    "name": f"{account.firstname} {account.lastname}",
                    "balance": account.balance
                })
            except Account.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Account not found"})

    elif request.method == "POST":
        account_number = request.POST.get("account")
        deposit_amount = request.POST.get("amount")

        if not account_number or not deposit_amount:
            return JsonResponse({"status": "error", "message": "Missing required fields"})

        try:
            account = Account.objects.get(account_number=account_number)
            deposit_amount = float(deposit_amount)

            # Update balance
            account.balance += deposit_amount
            account.save()

            # Log transaction
            Transaction.objects.create(
                account=account,
                transaction_type="deposit",
                amount=deposit_amount,
                balance_after=account.balance
            )

            # ✅ Return JSON response instead of redirecting
            return JsonResponse({
                "status": "success",
                "message": "Deposit Successful",
                "new_balance": account.balance
            })

        except Account.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Account not found"})

    return render(request, "custom_admin/deposit.html")


from django.http import JsonResponse
from django.shortcuts import render
from .models import Account, Transaction  # Ensure Transaction model is imported

def withdraw_view(request):
    if request.method == "GET":
        account_number = request.GET.get("account_number")
        if account_number:
            try:
                account = Account.objects.get(account_number=account_number)
                return JsonResponse({
                    "status": "success",
                    "name": f"{account.firstname} {account.lastname}",
                    "balance": account.balance
                })
            except Account.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Account not found"})

    elif request.method == "POST":
        account_number = request.POST.get("account")
        withdraw_amount = request.POST.get("amount")

        if not account_number or not withdraw_amount:
            return JsonResponse({"status": "error", "message": "Missing required fields"})

        try:
            account = Account.objects.get(account_number=account_number)
            withdraw_amount = float(withdraw_amount)

            if withdraw_amount > account.balance:
                return JsonResponse({"status": "error", "message": "Insufficient balance"})

            # Deduct balance
            account.balance -= withdraw_amount
            account.save()

            # Log transaction
            Transaction.objects.create(
                account=account,
                transaction_type="withdraw",
                amount=withdraw_amount,
                balance_after=account.balance
            )

            # ✅ Return JSON response instead of redirecting
            return JsonResponse({
                "status": "success",
                "message": "Withdrawal Successful",
                "new_balance": account.balance
            })

        except Account.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Account not found"})

    return render(request, "custom_admin/withdraw.html")

from django.http import JsonResponse
from django.shortcuts import render
from .models import Account, Transaction

def transfer_view(request):
    if request.method == "GET":
        account_number = request.GET.get("account_number")
        if account_number:
            try:
                account = Account.objects.get(account_number=account_number)
                return JsonResponse({
                    "status": "success",
                    "name": f"{account.firstname} {account.lastname}",
                    "balance": account.balance
                })
            except Account.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Account not found"})

    elif request.method == "POST":
        sender_account = request.POST.get("sender_account")
        receiver_account = request.POST.get("receiver_account")
        transfer_amount = request.POST.get("amount")

        if not sender_account or not receiver_account or not transfer_amount:
            return JsonResponse({"status": "error", "message": "Missing required fields"})

        if sender_account == receiver_account:
            return JsonResponse({"status": "error", "message": "Cannot transfer to the same account"})

        try:
            sender = Account.objects.get(account_number=sender_account)
            receiver = Account.objects.get(account_number=receiver_account)
            transfer_amount = float(transfer_amount)

            if sender.balance < transfer_amount:
                return JsonResponse({"status": "error", "message": "Insufficient balance"})

            sender.balance -= transfer_amount
            receiver.balance += transfer_amount
            sender.save()
            receiver.save()

            Transaction.objects.create(account=sender, transaction_type="transfer_out", amount=transfer_amount, balance_after=sender.balance)
            Transaction.objects.create(account=receiver, transaction_type="transfer_in", amount=transfer_amount, balance_after=receiver.balance)

            return JsonResponse({"status": "success", "new_balance": sender.balance})

        except Account.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid account number"})

    return render(request, "custom_admin/transfer.html")
