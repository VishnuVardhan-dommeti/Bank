import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random

@csrf_exempt  # Use this for testing, but configure CSRF properly in production
def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"success": False, "message": "Email is required"}, status=400)

            otp = random.randint(100000, 999999)
            request.session['otp'] = otp  # Store OTP in session for validation
            
            return JsonResponse({"success": True, "otp": otp})  # Simulate sending OTP
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)
    
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from .models import User, Account  # Adjust based on actual model names
from Custom_admin.serializers import UserSerializer, AccountSerializer

@api_view(['POST'])
def register_user(request):
    data = request.data
    
    # Create User entry
    user_data = {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "date_of_birth": data.get("date_of_birth"),
        "national_id": data.get("national_id"),
        "gender": data.get("gender"),
        "marital_status": data.get("marital_status"),
        "occupation": data.get("occupation"),
        "income": data.get("income"),
        "address": data.get("address"),
        "city": data.get("city"),
        "state": data.get("state"),
        "zip_code": data.get("zip_code"),
        "password": make_password(data.get("password"))
    }
    
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user = user_serializer.save()
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Create Account entry
    account_data = {
        "user": user.id,  # Assuming a ForeignKey relation to User
        "account_type": data.get("account_type"),
        "branch": data.get("branch"),
        "opening_date": data.get("opening_date"),
        "balance_amount": data.get("balance_amount"),
    }
    
    account_serializer = AccountSerializer(data=account_data)
    if account_serializer.is_valid():
        account_serializer.save()
    else:
        return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
