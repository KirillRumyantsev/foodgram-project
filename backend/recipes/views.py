from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import CustomPageNumberPagination
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer)
from .utils import get_shopping_list


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели рецепта.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        """
        Выбор сериализатора по действиям пользователя.
        """
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=('post', 'delete')
    )
    def favorite(self, request, pk=None):
        """
        Добавление и удаление рецепта из избранного.
        """
        if request.method == 'POST':
            return self.add_to(FavoriteRecipe, request.user, pk)
        else:
            return self.delete_from(FavoriteRecipe, request.user, pk)

    @action(
        detail=True,
        methods=('post', 'delete')
    )
    def shopping_cart(self, request, pk):
        """
        Добавление и удаление рецепта из списка покупок.
        """
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        else:
            return self.delete_from(ShoppingCart, request.user, pk)

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=('get',),
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """
        Загрузка списка покупок.
        """
        return get_shopping_list(request)


class IngredientsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели ингредиента.
    """

    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели тега.
    """

    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
