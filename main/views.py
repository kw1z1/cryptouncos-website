# main/views.py

from django.shortcuts import render

def index(request):
    # Эта функция (представление) отвечает за главную страницу
    return render(request, 'main/index.html')

def resources(request):
    # Эта функция отвечает за страницу "Полезные ресурсы"
    return render(request, 'main/resources.html')