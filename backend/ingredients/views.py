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
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
