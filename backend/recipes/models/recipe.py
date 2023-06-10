from django.db import models
from django.core.validators import MinValueValidator

from .ingredients import Ingredient
from .tags import Tag


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        blank=False
    )
    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        blank=False
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка',
        blank=False
    )
    text = models.TextField(
        verbose_name='Текстовое описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe',
        related_name='recipes',
        verbose_name='Список ингредиентов',
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagsRecipe',
        related_name='recipes',
        verbose_name='Список ингредиентов',
        blank=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин',
        validators=[MinValueValidator(
            1, 'Время приготовления не может быть меньше 1 минуты'
        )],
        blank=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe'
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
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )


class ShoppingCart(models.Model):
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
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='favorite_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='favorite_recipes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'
            )
        ]
