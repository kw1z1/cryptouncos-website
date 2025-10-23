# main/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post

def index(request):
    return render(request, 'main/index.html')

def resources(request):
    return render(request, 'main/resources.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} был успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def custom_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

# Новые функции для блога
def blog(request):
    posts = Post.objects.all()  # Получаем все статьи, отсортированные по дате (см. ordering в модели)
    return render(request, 'main/blog.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'main/post_detail.html', {'post': post})