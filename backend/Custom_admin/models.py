import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.db import models


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
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer",
        
        null=True,  # Temporary to allow migration
        blank=True
    )
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="customers")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    
    occupation = models.CharField(max_length=100, blank=True, null=True)
    income = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
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
    password = models.CharField(max_length=128)
    
    last_transaction_date = models.DateTimeField(null=True, blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Ensure password is hashed before saving."""
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

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
# 🔹 Transfer Out Model (money leaving an account)
class TransferOut(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transfers_out")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="incoming_transfers")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="transfer_out")

    class Meta:
        verbose_name_plural = "Transfers Out"

    def __str__(self):
        return f"Transfer Out - {self.amount} from {self.from_account.account_number}"

# 🔹 Transfer In Model (money arriving to an account)
class TransferIn(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="outgoing_transfers")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transfers_in")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="transfer_in")

    class Meta:
        verbose_name_plural = "Transfers In"

    def __str__(self):
        return f"Transfer In - {self.amount} to {self.to_account.account_number}"
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
