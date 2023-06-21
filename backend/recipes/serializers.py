from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions, serializers
from users.serializers import CustomUserSerializer

from .models.ingredients import Ingredient
from .models.recipe import (FavoriteRecipe, IngredientsRecipe, Recipe,
                            ShoppingCart)
from .models.tags import Tag


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ингредиента.
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели тега.
    """

    name = serializers.CharField(
        required=True,
    )
    slug = serializers.SlugField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для связанной модели
    ингредиента и рецепта.
    """

    id = serializers.SerializerMethodField(
        method_name='get_id'
    )
    name = serializers.SerializerMethodField(
        method_name='get_name'
    )
    measurement_unit = serializers.SerializerMethodField(
        method_name='get_measurement_unit'
    )

    def get_id(self, obj):
        """
        Получение id ингредиента.
        """
        return obj.ingredient.id

    def get_name(self, obj):
        """
        Получение имени ингредиента.
        """
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        """
        Получение единицы измерения ингредиента.
        """
        return obj.ingredient.measurement_unit

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateUpdateIngredientsRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и удаления ингредиента.
    """

    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Количество ингредиента должно быть 1 или более.'
            ),
        )
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения рецепта.
    """

    author = CustomUserSerializer(
        read_only=True
    )
    tags = TagSerializer(
        many=True
    )
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    def get_ingredients(self, obj):
        """
        Получение ингредиентов рецепта.
        """
        ingredients = IngredientsRecipe.objects.filter(recipe=obj)
        serializer = IngredientsRecipeSerializer(ingredients, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        """
        Получение избранных рецептов.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """
        Получение рецептов из списка покупок.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и изменения рецепта.
    """

    author = CustomUserSerializer(
        read_only=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = CreateUpdateIngredientsRecipeSerializer(
        many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Время приготовления должно быть 1 мин. или более.'
            ),
        )
    )

    def validate_tags(self, value):
        """
        Валидация тегов.
        """
        if not value:
            raise exceptions.ValidationError(
                'Нужно добавить хотя бы один тег.'
            )
        return value

    def validate_ingredients(self, value):
        """
        Валидация ингредиентов.
        """
        if not value:
            raise exceptions.ValidationError(
                'Нужно добавить хотя бы один ингредиент.'
            )

        ingredients = [item['id'] for item in value]
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise exceptions.ValidationError(
                    'У рецепта не может быть два одинаковых ингредиента.'
                )
        return value

    def create(self, validated_data):
        """
        Создание рецепта.
        """
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
            IngredientsRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        """
        Изменение рецепта.
        """
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()

            for ingredient in ingredients:
                amount = ingredient['amount']
                ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
                IngredientsRecipe.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient,
                    defaults={'amount': amount}
                )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Отображение рецепта после создания или изменения.
        """
        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Получение краткой версии рецепта.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
