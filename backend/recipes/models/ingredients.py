from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
        blank=False
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=10,
        blank=False
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
