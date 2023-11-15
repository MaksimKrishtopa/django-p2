
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, DesignRequestForm, RequestCategoryForm
from .models import DesignRequest, RequestCategory

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'catalog/registration.html', {'form': form})

def create_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            return redirect('user_dashboard')
    else:
        form = DesignRequestForm()
    return render(request, 'catalog/create_request.html', {'form': form})

def manage_categories(request):
    categories = RequestCategory.objects.all()
    form = RequestCategoryForm()

    if request.method == 'POST':
        form = RequestCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')

    return render(request, 'catalog/manage_categories.html', {'categories': categories, 'form': form})

def home(request):
    latest_completed_requests = DesignRequest.objects.filter(status='Completed').order_by('-timestamp')[:4]
    in_progress_count = DesignRequest.objects.filter(status='In Progress').count()
    return render(request, 'catalog/home.html', {'latest_completed_requests': latest_completed_requests, 'in_progress_count': in_progress_count})

@login_required
def user_dashboard(request):
    return render(request, 'catalog/user_dashboard.html')

@login_required
def my_requests(request):
    user_requests = DesignRequest.objects.filter(user=request.user)
    return render(request, 'catalog/my_requests.html', {'requests': user_requests})

@login_required
def create_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user
            new_request.save()
            return redirect('my_requests')
    else:
        form = DesignRequestForm()
    return render(request, 'catalog/create_request.html', {'form': form})

@login_required
def change_request_status(request, request_id, new_status):
    design_request = DesignRequest.objects.get(id=request_id)
    design_request.status = new_status
    design_request.save()
    return redirect('admin_dashboard')

@login_required
def manage_categories(request):
    # Логика для управления категориями (добавление, изменение, удаление)
    # ...

    return render(request, 'catalog/manage_categories.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Неправильный логин или пароль')
    return render(request, 'catalog/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация успешна! Теперь вы можете войти в систему.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'catalog/registration.html', {'form': form})

@staff_member_required
def admin_dashboard(request):
    all_requests = DesignRequest.objects.all()
    return render(request, 'catalog/admin_dashboard.html', {'requests': all_requests})