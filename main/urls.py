# main/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('resources/', views.resources, name='resources'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='main/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('blog/', views.blog, name='blog'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create-post/', views.create_post, name='create_post'),
    path('bitcoin-chart/', views.bitcoin_chart, name='bitcoin_chart'),  # ← ЭТА СТРОКА ДОЛЖНА БЫТЬ
]