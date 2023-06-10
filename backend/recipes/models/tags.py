from django.db import models


# CHOICES_COLOR = (
#         ('Orange', 'Рыжий'),
#         ('Green', 'Зеленый'),
#         ('Purple', 'Фиолетовый'),
# )


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=10,
        unique=True,
        blank=False
    )
    color = models.CharField(
        max_length=10,
        verbose_name='Цвет тега',
        unique=True,
        blank=False
    )
    slug = models.SlugField(
        verbose_name='Slug тега',
        max_length=10,
        unique=True,
        blank=False
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_slug'
            )
        ]

    def __str__(self):
        return self.name
