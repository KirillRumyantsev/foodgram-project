from django.contrib import admin

from .models import CustomUser, Follow


class UsersAdmin(admin.ModelAdmin):
    """
    Настройка админ-зоны для модели пользователя.
    """

    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = "-пусто-"


class FollowsAdmin(admin.ModelAdmin):
    """
    Настройка админ-зоны для модели подписки.
    """

    list_display = ('user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('user', 'author')
    empty_value_display = "-пусто-"


admin.site.register(CustomUser, UsersAdmin)
admin.site.register(Follow, FollowsAdmin)
