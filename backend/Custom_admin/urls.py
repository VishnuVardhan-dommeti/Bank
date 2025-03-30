from django.urls import path
from .views import custom_admin_login, custom_admin_logout
from .views import custom_admin_dashboard 
from .views import new_account
from .views import manage_account
from .views import edit_account, delete_account, transactions_view, deposit_view, withdraw_view, transfer_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', custom_admin_login, name='custom_admin_login'),
    path("dashboard/", custom_admin_dashboard, name="custom_admin_dashboard"),
 #   path("logout/", LogoutView.as_view(next_page="custom_admin_login"), name="logout"),
    path('new_account/', new_account, name='new_account'),
    path('manage-account/', manage_account, name='manage_account'),
    path('edit-account/<int:account_id>/', edit_account, name='edit_account'),
    path('delete-account/<int:account_id>/', delete_account, name='delete_account'),
    path('transactions/', transactions_view, name='transactions'),
    path('deposit/', deposit_view, name='deposit_view'),
    path('withdraw/', withdraw_view, name='withdraw_view'),
    path('transfer/', transfer_view, name='transfer_view'),
    path("logout/", custom_admin_logout, name="custom_admin_logout"),
]
