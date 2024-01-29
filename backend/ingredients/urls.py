from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import IngredientViewSet

router_v1 = SimpleRouter()

router_v1.register('ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router_v1.urls)),
]
