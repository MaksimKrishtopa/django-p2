from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def home(request):
    return render(request, 'catalog/home.html')

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
        form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'catalog/register.html', {'form': form, 'profile_form': profile_form})

@login_required
def profile(request):
    return render(request, 'catalog/profile.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')