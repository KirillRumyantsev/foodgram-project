from django.core.validators import MinValueValidator
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

from users.serializers import CustomUserSerializer
from .models import (FavoriteRecipe, Ingredient, IngredientsRecipe, Recipe,
                     ShoppingCart, Tag)


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

    id = serializers.IntegerField(
        source="ingredient.id",
        read_only=True
    )
    name = serializers.CharField(
        source="ingredient.name"
    )
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateUpdateIngredientsRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания изменения и удаления ингредиента.
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
        if len(ingredients) != len(set(ingredients)):
            raise ValidationError(
                'Ингредиенты в рецепте должны быть уникальными!'
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        """
        Создание рецепта.
        """
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        IngredientsRecipe.objects.bulk_create(
            [IngredientsRecipe(
                ingredient=Ingredient.objects.get(pk=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            )for ingredient in ingredients])
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Изменение рецепта.
        """
        tags = validated_data.pop('tags', None)
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients', None)
        instance.ingredients.clear()

        IngredientsRecipe.objects.bulk_create(
            [IngredientsRecipe(
                recipe=instance,
                ingredient=Ingredient.objects.get(pk=ingredient['id']),
                amount=ingredient['amount']
            )for ingredient in ingredients])
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
