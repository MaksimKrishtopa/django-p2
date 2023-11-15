
from catalog.models import UserProfile
from django.urls import path
from .views import home, user_dashboard, my_requests

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('my-requests/', my_requests, name='my_requests'),
    # Добавьте другие URL-шаблоны, если необходимо
]