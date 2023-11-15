
from catalog.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DesignRequest

# Здесь добавьте ваши представления (views)
# Пример:

def home(request):
    return render(request, 'catalog/home.html')

@login_required
def user_dashboard(request):
    # Ваши логика и данные для личного кабинета пользователя
    return render(request, 'catalog/user_dashboard.html')

@login_required
def my_requests(request):
    user_requests = DesignRequest.objects.filter(user=request.user)
    return render(request, 'catalog/my_requests.html', {'requests': user_requests})