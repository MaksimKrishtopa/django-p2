from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('create-request/', views.create_request, name='create_request'),
    path('change-request-status/<int:request_id>/<str:new_status>/', views.change_request_status, name='change_request_status'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('login/', views.login, name='login'),  # Вам может потребоваться добавить соответствующие представления и шаблоны для страницы входа
    path('logout/', views.logout, name='logout'),
    path('registration/', views.register, name='registration'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]