"""
URL configuration for BankingSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import home

from django.contrib.auth import views as auth_views

urlpatterns = [
    
    
    path('', home, name='home'),
   path('login/', views.login_view, name='login'),  # Changed from login to login_view
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('register/', views.register, name='register'),
   # path('logout/', views.user_logout, name='logoutt'),
    path('logout/',views.logout_view, name='logoutt'),
    path('dashboard/<str:username>/profile/', views.my_profile, name='profile'),
    path('dashboard/<str:username>/deposit/', views.deposit, name='deposit'),
    path('dashboard/<str:username>/withdraw/', views.withdraw, name='withdraw'),
    path('dashboard/<str:username>/transfer/', views.transfer, name='transfer'),
    path('dashboard/<str:username>/interest/', views.interest, name='interest'),
    path('interest/', views.interest, name='interest'),
    path('interest_summary/<str:username>/', views.interest_summary, name='interest_summary'),
    path('dashboard/<str:username>/statement/', views.statement, name='statement'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='accounts_login'),  # Add this
    path("verify-balance-password/", views.verify_balance_password, name="verify_balance_password"),
    path('download_statement/', views.download_statement_pdf, name='download_statement_pdf'),
    path('about/', views.about, name='about'),
    path('setting/<str:username>/', views.setting, name='setting'),
    path('custom_admin/', include('Custom_admin.urls')),
]
