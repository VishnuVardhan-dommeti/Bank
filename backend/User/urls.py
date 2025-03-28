from django.urls import path
from . import views

urlpatterns = [
    path("api/register/", views.register, name="register"),
    path("api/send-otp/", views.send_otp, name="send_otp"),
]
