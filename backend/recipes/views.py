from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Favorite, Purchase, Recipe, Tag
from .pagination import CustomPagination
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, PurchaseSerializer,
                          RecipeChangeSerializer, RecipeReadSerializer,
                          RecipeSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    serializer_class = RecipeReadSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """Определение класса сериализатора в зависимости от действия."""
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeChangeSerializer
        return self.serializer_class

    @action(
        detail=True, methods=['get', 'delete'],
        serializer_class=RecipeSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        """Обработка эндпоинта '/shopping_cart'
        управления списком покупок пользователя."""
        user = self.request.user
        recipe = self.get_object()
        serializer = self.get_serializer(recipe)
        purchase_serializer = PurchaseSerializer(
            context={
                'request': request
            },
            data={
                'user': user.id,
                'recipe': recipe.id
            }
        )
        purchase_serializer.is_valid(raise_exception=True)
        if request.method == 'GET':
            Purchase.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            purchase = get_object_or_404(Purchase, user=user, recipe=recipe)
            purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['get', 'delete'],
        serializer_class=RecipeSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        """Обработка эндпоинта '/favorite'
        управления списком избранных рецептовпользователя."""
        user = self.request.user
        recipe = self.get_object()
        serializer = self.get_serializer(recipe)
        favorite_serializer = FavoriteSerializer(
            context={
                'request': request
            },
            data={
                'user': user.id,
                'recipe': recipe.id
            }
        )
        favorite_serializer.is_valid(raise_exception=True)
        if request.method == 'GET':
            Favorite.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Метод для скачивания списка покупок.
        В ответе будут перечислены ингредиенты,
        их общее количество и единицы измерения.
        """
        user = self.request.user
        recipes = Recipe.objects.filter(purchases__user=user)
        ingredients = recipes.values(
            'ingredients__name',
            'ingredients__measurement_unit__name'
        ).order_by('ingredients__name').annotate(
            ingredients_total=Sum('amount_ingredients__amount')
        )
        response = ''
        for item in ingredients:
            response += (
                f'{item.get("ingredients__name")} - '
                f'{str(item.get("ingredients_total"))} '
                f'{item["ingredients__measurement_unit__name"]}\n'
            )
        return HttpResponse(response, content_type='text/plain; charset=UTF-8')
