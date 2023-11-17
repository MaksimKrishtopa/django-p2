from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, UserProfileForm

from django.contrib.auth import logout

from django.contrib import messages

from .forms import DesignRequestForm, CreateDesignRequestForm
from .models import DesignRequest, DesignCategory

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DesignRequest
from .forms import DesignRequestForm
from django.shortcuts import get_object_or_404


def home(request):
    # Получаем последние 4 выполненные заявки
    last_completed_requests = DesignRequest.objects.filter(status='Выполнено').order_by('-timestamp')[:4]

    # Получаем количество заявок в статусе 'In Progress'
    in_progress_count = DesignRequest.objects.filter(status='В работе').count()

    context = {
        'last_completed_requests': last_completed_requests,
        'in_progress_count': in_progress_count,
    }

    return render(request, 'catalog/home.html', context)




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



@login_required
def create_design_request(request):
    if request.method == 'POST':
        form = CreateDesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.status = 'Новая'
            design_request.save()
            return redirect('design_request_list')
    else:
        form = CreateDesignRequestForm()

    return render(request, 'catalog/create_design_request.html', {'form': form})


@login_required
def view_design_requests(request):
    status = request.GET.get('status', 'all')

    if status == 'all':
        design_requests = DesignRequest.objects.filter(user=request.user)
    else:
        design_requests = DesignRequest.objects.filter(user=request.user, status=status)

    return render(request, 'catalog/view_design_requests.html', {'design_requests': design_requests})


@login_required(login_url='/login/')
def design_request_list(request):
    design_requests = DesignRequest.objects.filter(user=request.user.id)
    return render(request, 'catalog/design_request_list.html', {'design_requests': design_requests})


def delete_design_request(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk, user=request.user)

    if request.method == 'POST':
        design_request.delete()
        messages.success(request, 'Заявка успешно удалена.')
        return redirect('design_request_list')

    return render(request, 'catalog/design_request_confirm_delete.html', {'design_request': design_request})


@login_required
def change_status(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk, user=request.user, status='Новая')

    if request.method == 'POST':
        status = request.POST.get('status', 'In Progress')

        # Проверка статуса
        if status == 'Completed':
            image = request.FILES.get('image')
            if not image:
                messages.error(request, 'Добавьте изображение дизайна для статуса "Выполнено".')
                return redirect('change_status', pk=pk)

        design_request.status = status
        design_request.save()

        return redirect('view_design_requests')

    return render(request, 'catalog/change_status.html', {'design_request': design_request})


@login_required
def manage_categories(request):
    categories = DesignCategory.objects.all()
    return render(request, 'catalog/manage_categories.html', {'categories': categories})
