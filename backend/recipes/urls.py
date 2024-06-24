from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagViewSet

router_v1 = DefaultRouter()
router_v1.register(r'recipes', RecipeViewSet, basename='recipe')
router_v1.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'recipes/download_shopping_cart/',
        RecipeViewSet.as_view({'get': 'download_shopping_cart'}),
        name='download_shopping_cart'
    ),
    path(
        'recipes/<int:pk>/shopping_cart/',
        RecipeViewSet.as_view({'get': 'shopping_cart', 'delete': 'shopping_cart'}),
        name='recipe_shopping_cart'
    ),
    path(
        'recipes/<int:pk>/favorite/',
        RecipeViewSet.as_view({'get': 'favorite', 'delete': 'favorite'}),
        name='recipe_favorite'
    ),
]
