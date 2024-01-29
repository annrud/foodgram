from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для представления единиц измерений и наименований ингредиентов."""
    # Отображение measurement_unit в виде строки
    measurement_unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        # Определяем модель, с которой работает сериализатор
        model = Ingredient
        # Список полей модели, которые будут сериализованы и доступны в API
        fields = ('id', 'name', 'measurement_unit')

        validators = [
            # Гарантирует уникальность комбинации полей measurement_unit и name
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(),
                fields=['measurement_unit', 'name']
            )
        ]
