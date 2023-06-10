from django.contrib import admin

from .models.recipe import Recipe
from .models.tags import Tag
from .models.ingredients import Ingredient


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')
    empty_value_display = "-пусто-"


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
