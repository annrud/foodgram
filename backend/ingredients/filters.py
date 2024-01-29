from django_filters import rest_framework as filters

from .models import Ingredient


class IngredientFilter(filters.FilterSet):
    # Создание фильтрации name, т.е.
    # наименованию ингредиента должно начинаться с того, что указано в параметре name,
    # например /api/ingredients/?name=Tomato
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        # Создание фильтра для модели Ingredient с одним фильтром по полю name
        model = Ingredient
        fields = ['name']
