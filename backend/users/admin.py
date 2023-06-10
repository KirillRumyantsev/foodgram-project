from django.contrib import admin

from .models import CustomUser


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = "-пусто-"


admin.site.register(CustomUser, UsersAdmin)
