from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from Custom_admin.models import Customer, Address, Account, Branch, AccountType
from Custom_admin.serializers import CustomerSerializer, AddressSerializer, AccountSerializer, BalanceSerializer





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import random

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

from django.contrib.auth import authenticate, login as auth_login  # Rename to avoid conflict
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Changed from 'username' to 'email'
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please fill in both email and password')
            return render(request, 'login.html')
        
        # Authenticate using email as username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)  # Using renamed import
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')

@login_required
def dashboard(request, username):
    if request.user.username != username:
        return redirect('login')
    return render(request, 'dashboard.html', {'username': username})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db import transaction as db_transaction
from Custom_admin.models import Customer, Address, Account, Balance, AccountType, Branch, Transaction, Deposit
from Custom_admin.serializers import CustomerSerializer, AddressSerializer, AccountSerializer
import random
import string
from datetime import datetime

def generate_account_number():
    """Generate exactly 12 uppercase alphanumeric characters"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def register(request):
    # Ensure required AccountTypes and Branches exist
    AccountType.objects.get_or_create(name='savings', defaults={'min_balance': 500.00, 'interest_rate': 0.50})
    AccountType.objects.get_or_create(name='current', defaults={'min_balance': 1000.00, 'interest_rate': 0.25})
    
    branches = ['main', 'north', 'south', 'east']
    for branch in branches:
        Branch.objects.get_or_create(branch_name=branch, defaults={'location': f"{branch.capitalize()} Location"})

    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Add password validation
        if not password or password != confirm_password:
            messages.error(request, 'Passwords do not match or are empty')
            return redirect('register')
        
        # Preliminary checks
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        if Customer.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already exists')
            return redirect('register')

        try:
            with db_transaction.atomic():
                # Generate UNIQUE 12-character account number
                account_number = generate_account_number()
                while Account.objects.filter(account_number=account_number).exists():
                    account_number = generate_account_number()

                # 1. Create Customer
                customer = Customer.objects.create(
                    first_name=request.POST.get('firstname'),
                    last_name=request.POST.get('lastname'),
                    email=email,
                    phone=phone,
                    date_of_birth=request.POST.get('dob'),
                    gender=request.POST.get('gender').capitalize(),
                    occupation=request.POST.get('occupation'),
                    income=float(request.POST.get('income', 0.00))
                )

                # 2. Create Address
                Address.objects.create(
                    customer=customer,
                    street=request.POST.get('address'),
                    city=request.POST.get('city'),
                    state=request.POST.get('state'),
                    zip_code=request.POST.get('zipcode'),
                    country=request.POST.get('country')
                )

                # 3. Get Account Type and Branch
                account_type = AccountType.objects.get(name=request.POST.get('account_type').lower())
                branch = Branch.objects.get(branch_name=request.POST.get('branch').lower())

                # 4. Create Account - let the model handle password hashing
                account = Account.objects.create(
                    customer=customer,
                    account_type=account_type,
                    branch=branch,
                    account_number=account_number,
                    balance_amount=float(request.POST.get('initial_deposit', 0.00)),
                    password=make_password(password),  # Will be hashed by model's save()
                    last_transaction_date=datetime.now()
                )

                # 5. Create Balance
                Balance.objects.create(
                    account=account,
                    balance=float(request.POST.get('initial_deposit', 0.00))
                )

                # 6. Create Transaction if deposit > 0
                initial_deposit = float(request.POST.get('initial_deposit', 0.00))
                if initial_deposit > 0:
                    deposit_txn = Transaction.objects.create(
                        account=account,
                        transaction_type='Deposit',
                        amount=initial_deposit
                    )
                    Deposit.objects.create(transaction=deposit_txn)

                messages.success(request, f'Account created successfully! Account Number: {account_number}')
                return redirect('login')

        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('register')

    return render(request, 'register.html')

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Process password reset
            messages.success(request, 'Password reset link sent to your email')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def my_profile(request, username):
    if request.user.username != username:
        return redirect('login')
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form, 'username': username})

@login_required
def deposit(request, username):
    if request.user.username != username:
        return redirect('login')
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            # Process deposit
            messages.success(request, f'${amount} deposited successfully')
            return redirect('dashboard', username=username)
    else:
        form = DepositForm()
    return render(request, 'deposit.html', {'form': form, 'username': username})

@login_required
def withdraw(request, username):
    if request.user.username != username:
        return redirect('login')
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            # Process withdrawal
            messages.success(request, f'${amount} withdrawn successfully')
            return redirect('dashboard', username=username)
    else:
        form = WithdrawForm()
    return render(request, 'withdraw.html', {'form': form, 'username': username})

@login_required
def transfer(request, username):
    if request.user.username != username:
        return redirect('login')
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient = form.cleaned_data['recipient']
            # Process transfer
            messages.success(request, f'${amount} transferred to {recipient}')
            return redirect('dashboard', username=username)
    else:
        form = TransferForm()
    return render(request, 'transfer.html', {'form': form, 'username': username})

@login_required
def interest(request, username):
    if request.user.username != username:
        return redirect('login')
    # Calculate interest
    interest_amount = random.uniform(5, 50)
    return render(request, 'interest.html', {'interest': interest_amount, 'username': username})

def interest_summary(request, username):
    if not request.user.is_authenticated or request.user.username != username:
        return redirect('login')
    # Get interest history
    interests = Interest.objects.filter(user=request.user).order_by('-date')[:10]
    return render(request, 'interest_summary.html', {'interests': interests, 'username': username})

@login_required
def statement(request, username):
    if request.user.username != username:
        return redirect('login')
    # Get transaction history
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:30]
    return render(request, 'statement.html', {'transactions': transactions, 'username': username})

def verify_balance_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            return JsonResponse({'valid': True})
        return JsonResponse({'valid': False})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def download_statement_pdf(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:30]
    html = render_to_string('statement_pdf.html', {'transactions': transactions, 'user': request.user})
    
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }
    
    pdf = pdfkit.from_string(html, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="statement.pdf"'
    return response

def about(request):
    return render(request, 'about.html')

@login_required
def setting(request, username):
    if request.user.username != username:
        return redirect('login')
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully')
    else:
        form = SettingsForm(instance=request.user)
    return render(request, 'settings.html', {'form': form, 'username': username})