# main/models.py

from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    summary = models.TextField(max_length=500, verbose_name='Краткое содержание')
    content = models.TextField(verbose_name='Полное содержание')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-date_posted']  # Сортировка по убыванию даты
    
    def __str__(self):
        return self.title