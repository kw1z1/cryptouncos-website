# main/forms.py

from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Напишите ваш комментарий...',
                'rows': 4
            }),
        }
        labels = {
            'text': 'Ваш комментарий'
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'summary', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите заголовок статьи...'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Введите краткое содержание...',
                'rows': 3
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Введите полное содержание статьи...',
                'rows': 10
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input'
            })
        }
        labels = {
            'title': 'Заголовок статьи',
            'summary': 'Краткое содержание',
            'content': 'Полное содержание',
            'image': 'Изображение для статьи'
        }