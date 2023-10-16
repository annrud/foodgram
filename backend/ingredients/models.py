from django.db import models
from django.db.models import UniqueConstraint


class Unit(models.Model):
    """Модель единиц измерения."""
    # Хранение названия единицы измерения
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Единицы измерения'
    )
    # Определено человекочитаемое имя для модели
    # в единственном и множественном числе
    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
    # Cтроковое представление объекта
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    # Хранение названия ингредиента
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    # Внешний ключ связывает ингредиент с моделью Unit,
    # определяя, какая единица измерения используется для этого ингредиента.
    # Параметр on_delete=models.CASCADE указывает на удаление ингредиента,
    # если соответствующая единица измерения будет удалена.
    # Параметр related_name='ingredients' позволяет обращаться
    # к связанным ингредиентам из объектов модели Unit.
    measurement_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )

    # Определен UniqueConstraint, который гарантирует
    # уникальность сочетания полей measurement_unit и name.
    # Это означает, что для каждого ингредиента должна
    # быть только одна единица измерения.
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['measurement_unit', 'name'],
                name='unique_name_measurement_unit'
            ),
        ]

    # Cтроковое представление объекта
    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'
