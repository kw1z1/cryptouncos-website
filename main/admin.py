# main/admin.py

from django.contrib import admin
from django.contrib.auth.models import User, Group

# Настройка отображения пользователей
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Перерегистрируем User с нашей настройкой
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