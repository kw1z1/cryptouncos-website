# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'), # Главная страница (http://127.0.0.1:8000/)
    path('resources/', views.resources, name='resources'), # Страница ресурсов
]