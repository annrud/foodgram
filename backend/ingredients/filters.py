from django_filters import rest_framework as filters

from .models import Ingredient


class IngredientFilter(filters.FilterSet):
    """Класс для создания фильтрации по наименованию ингредиента."""
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']
