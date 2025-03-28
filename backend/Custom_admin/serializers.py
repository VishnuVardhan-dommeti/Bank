from rest_framework import serializers
from .models import (
    Account, Customer, Address, Transaction, Withdraw, Deposit, 
    TransferIn, TransferOut, AccountType, Balance, Login, Logout
)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = '__all__'

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'

class TransferInSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferIn
        fields = '__all__'

class TransferOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferOut
        fields = '__all__'

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'

class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logout
        fields = '__all__'
