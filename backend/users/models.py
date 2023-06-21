from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    """

    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким username уже существует.',
        }
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.',
        }
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'password',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_auth'
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """
    Модель подписки.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        CustomUser, null=True,
        on_delete=models.CASCADE,
        related_name='followed',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['author', 'user'],
            name='unique_object'
        )]
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
