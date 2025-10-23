# main/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    summary = models.TextField(max_length=500, verbose_name='Краткое содержание')
    content = models.TextField(verbose_name='Полное содержание')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name='Изображение')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-date_posted']
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата комментария')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_date']
    
    def __str__(self):
        return f'Комментарий от {self.author} к "{self.post.title}"'