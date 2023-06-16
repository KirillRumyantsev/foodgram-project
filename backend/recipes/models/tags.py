from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=10,
        unique=True,
    )
    color = models.CharField(
        max_length=10,
        verbose_name='Цвет тега',
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Slug тега',
        max_length=10,
        unique=True,
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
