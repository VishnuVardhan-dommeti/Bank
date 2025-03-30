from rest_framework import serializers
from .models import Customer, Address, Account, Balance, AccountType, Branch, Transaction

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 
                'date_of_birth', 'gender', 'occupation', 'income', 'employee']
        extra_kwargs = {
            'email': {'required': True},
            'phone': {'required': True},
            'gender': {'required': True},
            'date_of_birth': {'required': True}
        }

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'customer', 'street', 'city', 'state', 
                 'zip_code', 'country', 'created_at']
        extra_kwargs = {
            'customer': {'required': True},
            'street': {'required': True},
            'city': {'required': True}
        }

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'customer', 'account_type', 'branch', 'account_number',
                 'balance_amount', 'password', 'last_transaction_date', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'account_number': {'read_only': True},
            'customer': {'required': True},
            'account_type': {'required': True},
            'branch': {'required': True}
        }

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id', 'account', 'balance', 'updated_at']
        extra_kwargs = {
            'account': {'required': True}
        }