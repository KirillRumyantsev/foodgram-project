from rest_framework import serializers, validators
from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer
)

from recipes.serializers import RecipeSerializer
from recipes.models.recipe import Recipe
from .models import CustomUser, Follow
from .mixins import IsSubscribedMixin


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = CustomUser
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user

        if user.is_anonymous:
            return False

        return Follow.objects.filter(user=user, author=obj).exists()

    class Meta:
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        ]
        model = CustomUser


class UserSubscribeSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField('get_recipes_count')
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=CustomUser.objects.all()
        )]
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'recipes', 'recipes_count', 'is_subscribed'
        ]

    def validate(self, data):
        author = data['followed']
        user = data['follower']
        if user == author:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        if (Follow.objects.filter(author=author, user=user).exists()):
            raise serializers.ValidationError('Вы уже подписались!')
        return data

    def create(self, validated_data):
        subscribe = Follow.objects.create(**validated_data)
        subscribe.save()
        return subscribe

    def get_recipes_count(self, data):
        return Recipe.objects.filter(author=data).count()

    def get_recipes(self, data):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        recipes = (
            data.recipes.all()[:int(recipes_limit)]
            if recipes_limit else data.recipes
        )
        serializer = serializers.ListSerializer(child=RecipeSerializer())
        return serializer.to_representation(recipes)
