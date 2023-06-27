from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    """
    Фильтрация ингредиентов по полю name.
    """

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    """
    Фильтрация рецептов по тегам,
    избранному и списку покупок.
    """

    is_favorited = filters.BooleanFilter(
        method='get_favorite',
        label='favorite',
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='tags',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart',
        label='shopping_cart',
    )

    def get_favorite(self, queryset, name, value):
        """
        Фильтрация по избранным рецептам.
        """
        if value:
            return queryset.filter(
                favorite_recipes__user=self.request.user
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """
        Фильтрация по списку покупок.
        """
        if value:
            return queryset.filter(
                shopping_cart__user=self.request.user
            )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',
                  'is_favorited', 'is_in_shopping_cart',)
