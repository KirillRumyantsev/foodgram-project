from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .models.recipe import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                            Tag)
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer)
from .utils import get_shopping_list


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    permission_classes = (AuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer

        return RecipeSerializer

    @action(detail=True, methods=('post', 'delete'))
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.request.method == 'POST':
            if FavoriteRecipe.objects.filter(
                    user=user,
                    recipe=recipe
            ).exists():
                raise exceptions.ValidationError('Рецепт уже в избранном.')
            FavoriteRecipe.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(
                recipe,
                context={'request': request}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            favorite = get_object_or_404(
                FavoriteRecipe,
                user=user,
                recipe=recipe
            )
            favorite.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.request.method == 'POST':
            if ShoppingCart.objects.filter(
                    user=user,
                    recipe=recipe
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже в списке покупок.'
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(
                recipe,
                context={'request': request}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                    user=user,
                    recipe=recipe
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепта нет в списке покупок, либо он уже удален.'
                )
            shopping_cart = get_object_or_404(
                ShoppingCart,
                user=user,
                recipe=recipe
            )
            shopping_cart.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        try:
            return get_shopping_list(request)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
