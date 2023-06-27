from django.contrib import admin

from .models import Ingredient, IngredientsRecipe, Recipe, Tag


class IngredientsInline(admin.TabularInline):
    """
    Получение поля из связанной модели
    ингредиента и рецепта.
    """

    model = IngredientsRecipe
    extra = 1


class TagsInline(admin.TabularInline):
    """
    Получение поля из связанной модели
    тега и рецепта.
    """

    model = Recipe.tags.through
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    """
    Настройка админ-зоны для модели рецепта.
    """

    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = "-пусто-"
    inlines = [
        TagsInline, IngredientsInline
    ]
    readonly_fields = ['count_recipes_favorite']

    def count_recipes_favorite(self, obj):
        """
        Получение количества добавлений
        рецепта в избранное.
        """
        return obj.favorite_recipes.count()

    count_recipes_favorite.short_description = 'Популярность'


class TagsAdmin(admin.ModelAdmin):
    """
    Настройка админ-зоны для модели тега.
    """

    list_display = ('name', 'color')
    list_filter = ('name',)
    search_fields = ('name',)
    inlines = [
        TagsInline
    ]
    exclude = ('tags',)


class IngredientsAdmin(admin.ModelAdmin):
    """
    Настройка админ-зоны для модели ингредиента.
    """

    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    inlines = [
        IngredientsInline
    ]


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
