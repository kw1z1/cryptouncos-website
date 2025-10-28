# main/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm, PostForm
from .services import CryptoService  # ← ДОБАВЬТЕ ЭТУ СТРОКУ

def index(request):
    crypto_prices = CryptoService.get_crypto_prices()  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
    return render(request, 'main/index.html', {'crypto_prices': crypto_prices})  # ← ИЗМЕНИТЕ ЭТУ СТРОКУ

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

def blog(request):
    posts = Post.objects.all()
    return render(request, 'main/blog.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Для добавления комментария необходимо войти в систему.')
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Ваш комментарий был успешно добавлен!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'main/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

# Новое представление для создания статей
@login_required
def create_post(request):
    # Проверяем, что пользователь - администратор
    if not request.user.is_staff:
        messages.error(request, 'Только администраторы могут добавлять статьи.')
        return redirect('blog')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Статья "{post.title}" была успешно создана!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    return render(request, 'main/create_post.html', {'form': form})

# ДОБАВЬТЕ ЭТУ ФУНКЦИЮ В КОНЕЦ ФАЙЛА ↓
def bitcoin_chart(request):
    from .services import CryptoService
    
    # Получаем данные для графика
    days = int(request.GET.get('days', 30))
    chart_data = CryptoService.get_bitcoin_chart_data(days)
    indicators = CryptoService.calculate_indicators(chart_data)
    
    return render(request, 'main/bitcoin_chart.html', {
        'chart_data': chart_data,
        'indicators': indicators,
        'timeframe': days
    })