from django.urls import path, include

from . import views
from .views import home, login_user, register_user, profile, logout_user, create_design_request, design_request_list, delete_design_request, view_design_requests
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login_user'),
    path('register/', register_user, name='register_user'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_user, name='logout_user'),
    path('create/', create_design_request, name='create_design_request'),
    path('list/', design_request_list, name='design_request_list'),
    path('delete/<int:pk>/', delete_design_request, name='delete_design_request'),
    path('view/', view_design_requests, name='view_design_requests'),  # добавим новый URL для просмотра заявок

]