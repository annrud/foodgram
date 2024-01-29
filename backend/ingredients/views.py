from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from .filters import IngredientFilter
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    # Устанавливаем сериализатор
    serializer_class = IngredientSerializer
    # Объекты из базы данных для обработки этим представлением
    queryset = Ingredient.objects.all()
    # Для представления не используется пагинация
    pagination_class = None
    # Настройка фильтрации
    filter_backends = (DjangoFilterBackend,)
    # Определяем набор фильтров, который будет применен к queryset
    filterset_class = IngredientFilter
