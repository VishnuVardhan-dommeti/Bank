from django.contrib import admin
from .models import (
    Branch, Employee, Customer, Address,
    AccountType, Account, Transaction,
    Withdraw, Deposit, Transfer,
    Balance, Login, Logout,
    EditAccount, Announcements, InterestTable
)

admin.site.register(Branch)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(AccountType)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Withdraw)
admin.site.register(Deposit)
admin.site.register(Transfer)
admin.site.register(Balance)
admin.site.register(Login)
admin.site.register(Logout)
admin.site.register(EditAccount)
admin.site.register(Announcements)
admin.site.register(InterestTable)

# Custom titles for admin site
admin.site.site_header = "Banking Management Admin"
admin.site.site_title = "Banking Admin Portal"
admin.site.index_title = "Welcome to the Admin Panel"
