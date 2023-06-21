from django.core.validators import MinValueValidator
from django.db import models

from .ingredients import Ingredient
from .tags import Tag


class Recipe(models.Model):
    """
    Модель рецепта.
    """

    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
    )
    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка',
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe',
        related_name='recipes',
        verbose_name='Список ингредиентов',
        blank=False,
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagsRecipe',
        related_name='recipes',
        verbose_name='Тег',
        blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин',
        validators=[MinValueValidator(
            1, 'Время приготовления не может быть меньше 1 минуты'
        )],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    """
    Связанная модель ингредиента и рецепта.
    """

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text='Количество ингредиента',
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe'
            )
        ]


class TagsRecipe(models.Model):
    """
    Связанная модель тега и рецепта.
    """

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class ShoppingCart(models.Model):
    """
    Модель списка покупок.
    """

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_cart'
            )
        ]


class FavoriteRecipe(models.Model):
    """
    Модель избранного рецепта.
    """

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='favorite_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'
            )
        ]
