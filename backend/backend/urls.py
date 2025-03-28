from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom_admin/', include('Custom_admin.urls')),
]
