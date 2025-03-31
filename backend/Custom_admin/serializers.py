from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer, Address, Account, Balance, AccountType, Branch, Transaction

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['first_name']+validated_data['last_name'],  # Use email as username
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
    
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'user', 'employee', 'first_name', 'last_name', 'email', 'phone', 
                'date_of_birth', 'gender', 'occupation', 'income']
        extra_kwargs = {
            'email': {'required': True},
            'phone': {'required': True},
            'gender': {'required': True},
            'date_of_birth': {'required': True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

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