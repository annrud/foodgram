import csv

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient, Unit


class Command(BaseCommand):
    help = 'Load ingredients data to BD'

    # Метод handle вызывается при выполнении команды
    def handle(self, *args, **options):
        """Обрабатывает каждую строку в CSV-файле,
        создавая записи в базе данных для каждого ингредиента
        и его единицы измерения.
        """
        # Открывает CSV-файл с ингредиентами
        with open(
                'ingredients/data/ingredients.csv',
                encoding='utf-8'
        ) as f:
            # Чтения строк из открытого CSV-файла
            reader = csv.reader(f)
            for row in reader:
                name, measurement_unit_name = row
                if len(measurement_unit_name.strip()) == 0:
                    continue
                # Получает из базы данных или создает запись в Unit
                # с указанным названием единицы измерения
                measurement_unit, _ = Unit.objects.get_or_create(
                    name=measurement_unit_name
                )
                # Получает или создает запись в модели Ingredient
                # с указанным названием ингредиента
                # и связанной единицей измерения
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=measurement_unit
                )
