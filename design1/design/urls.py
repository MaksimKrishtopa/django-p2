from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('superadmin', admin.site.urls),
    path('', include('catalog.urls')),
]