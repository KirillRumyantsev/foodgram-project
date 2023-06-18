import json

from django.core.management.base import BaseCommand

from recipes.models.ingredients import Ingredient


class Command(BaseCommand):
    help = 'Заполнение ингридиентов из json файла'

    def handle(self, *args, **kwargs):
        with open('data/ingredients.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for row in data:
            account = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            account.save()
