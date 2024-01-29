from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagViewSet

router_v1 = DefaultRouter()
# Обработка следующих путей:
# http://localhost/api/recipes/
# http://localhost/api/recipes/{id}/
router_v1.register(r'recipes', RecipeViewSet, basename='recipe')
# Обработка следующих путей:
# http://localhost/api/tags/
# http://localhost/api/tags/{id}/
router_v1.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router_v1.urls)),
    # Скачать файл со списком покупок
    path(
        'recipes/download_shopping_cart/',
        RecipeViewSet.as_view({'get': 'download_shopping_cart'}),
        name='download_shopping_cart'
    ),
    # Добавление/удаление рецепта (по идентификатору) в список покупок
    path(
        'recipes/<int:pk>/shopping_cart/',
        RecipeViewSet.as_view({'get': 'shopping_cart', 'delete': 'shopping_cart'}),
        name='recipe_shopping_cart'
    ),
    # Добавление/удаление рецепта (по идентификатору) в избранное
    path(
        'recipes/<int:pk>/favorite/',
        RecipeViewSet.as_view({'get': 'favorite', 'delete': 'favorite'}),
        name='recipe_favorite'
    ),
]
