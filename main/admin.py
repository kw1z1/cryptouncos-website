# main/admin.py

from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Post, Comment

# Настройка отображения статей
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'summary_preview')
    list_filter = ('date_posted',)
    search_fields = ('title', 'content')
    date_hierarchy = 'date_posted'
    
    def summary_preview(self, obj):
        return obj.summary[:100] + '...' if len(obj.summary) > 100 else obj.summary
    summary_preview.short_description = 'Краткое содержание'

admin.site.register(Post, PostAdmin)

# Настройка отображения комментариев
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_date', 'text_preview')
    list_filter = ('created_date', 'author')
    search_fields = ('text', 'author__username', 'post__title')
    date_hierarchy = 'created_date'
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Текст комментария'

admin.site.register(Comment, CommentAdmin)

# Остальной код админки остается без изменений...

# Настройка отображения пользователей
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Настройка отображения групп
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

# Настройка заголовков админки
admin.site.site_header = "Панель управления CryptoUncos"
admin.site.site_title = "Админка CryptoUncos"
admin.site.index_title = "Добро пожаловать в панель управления"