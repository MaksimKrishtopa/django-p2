from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import DesignRequest
def home(request):
    # Получаем последние 4 заявки в статусе "Выполнено"
    latest_requests = DesignRequest.objects.filter(status='Completed').order_by('-timestamp')[:4]

    # Получаем количество заявок в статусе "Принято в работу"
    in_progress_count = DesignRequest.objects.filter(status='In Progress').count()

    return render(request, 'catalog/home.html', {'latest_requests': latest_requests, 'in_progress_count': in_progress_count})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'catalog/login.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('home')

    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()

    return render(request, 'catalog/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    return render(request, 'catalog/profile.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')