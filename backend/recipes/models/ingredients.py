from django.db import models


class Ingredient(models.Model):
    """
    Модель ингредиента.
    """

    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return self.name
