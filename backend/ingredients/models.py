from django.db import models
from django.db.models import UniqueConstraint


class Unit(models.Model):
    """Модель единиц измерения."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['measurement_unit', 'name'],
                name='unique_name_measurement_unit'
            ),
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'
