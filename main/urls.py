# main/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('resources/', views.resources, name='resources'),
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),  # Вход
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Выход
]