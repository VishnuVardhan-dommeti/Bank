import uuid
from django.db import models
from django.contrib.auth.models import User

# 🔹 Branch Model
class Branch(models.Model):
    branch_name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.branch_name

# 🔹 Employee Model
class Employee(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="employees")
    supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="subordinates")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    hire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"

# 🔹 Customer Model
class Customer(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="customers")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    national_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    marital_status = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')])
    occupation = models.CharField(max_length=100, blank=True, null=True)
    income = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    risk_category = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 🔹 Address Model
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

# 🔹 Account Type Model
class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    min_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 🔹 Account Model
class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="accounts")
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name="accounts")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=12, unique=True, editable=False, default=uuid.uuid4)
    balance_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    overdraft_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    last_transaction_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Dormant', 'Dormant'), ('Closed', 'Closed')], default='Active')
    opening_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number} - {self.customer.first_name} {self.customer.last_name}"

# 🔹 Transactions Model
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
        ('Transfer In', 'Transfer In'),
        ('Transfer Out', 'Transfer Out'),
        ('Interest', 'Interest')
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.account.account_number}"

# 🔹 Withdraw Model
class Withdraw(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)

# 🔹 Deposit Model
class Deposit(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)

# 🔹 Transfer Model
class Transfer(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transfers_out")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transfers_in")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

# 🔹 Balance Model
class Balance(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="balance")
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

# 🔹 Login Model
class Login(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# 🔹 Logout Model
class Logout(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# 🔹 Edit Account Model
class EditAccount(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    modified_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    modification_details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# 🔹 Announcements Model
class Announcements(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 🔹 Interest Table Model
class InterestTable(models.Model):
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
