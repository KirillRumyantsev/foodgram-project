from rest_framework import serializers, validators
from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer
)

from .models import CustomUser


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = CustomUser
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name'
        ]
        model = CustomUser
