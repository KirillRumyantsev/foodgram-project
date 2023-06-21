from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models.recipe import Recipe
from rest_framework import serializers

from .models import CustomUser, Follow


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания пользователя
    наследуется от djoser.serializers.
    """

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор для модели пользователя,
    дополнительно реализован вывод поля is_subscribed.
    """

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    def get_is_subscribed(self, obj):
        """
        Отображение подписки на автора.
        """
        user = self.context['request'].user

        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class SubscriptionSerializer(CustomUserSerializer):
    """
    Сериализатор для подписок.
    """

    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    def get_srs(self):
        """
        Краткий вывод полей, импортируется из
        recipes.serializers (импорт в методе для избавления от
        цикличного импорта).
        """
        from recipes.serializers import ShortRecipeSerializer
        return ShortRecipeSerializer

    def get_recipes(self, obj):
        """
        Получение рецептов автора.
        """
        author_recipes = Recipe.objects.filter(author=obj)

        if 'recipes_limit' in self.context.get('request').GET:
            recipes_limit = self.context.get('request').GET['recipes_limit']
            author_recipes = author_recipes[:int(recipes_limit)]

        if author_recipes:
            serializer = self.get_srs()(
                author_recipes,
                context={'request': self.context.get('request')},
                many=True
            )
            return serializer.data
        return []

    def get_recipes_count(self, obj):
        """
        Получение количества рецептов автора.
        """
        return Recipe.objects.filter(author=obj).count()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_subscribed', 'recipes', 'recipes_count')
