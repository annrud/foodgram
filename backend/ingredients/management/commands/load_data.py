import csv

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient, Unit


class Command(BaseCommand):
    help = 'Load ingredients data to BD'

    def handle(self, *args, **options):
        """Обрабатывает каждую строку в CSV-файле,
        создавая записи в базе данных для каждого ингредиента
        и его единицы измерения.
        """
        with open(
                'ingredients/data/ingredients.csv',
                encoding='utf-8'
        ) as f:
            reader = csv.reader(f)
            for row in reader:
                name, measurement_unit_name = row
                if len(measurement_unit_name.strip()) == 0:
                    continue
                measurement_unit, _ = Unit.objects.get_or_create(
                    name=measurement_unit_name
                )
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=measurement_unit
                )
