from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для представления единиц измерений и наименований ингредиентов."""
    measurement_unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

        validators = [
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(),
                fields=['measurement_unit', 'name']
            )
        ]
