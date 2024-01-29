from django.urls import include, path
from djoser import views
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router_v1 = DefaultRouter()
# Обработка следующих путей:
# http://localhost/api/users/
# http://localhost/api/users/{id}/
# http://localhost/api/users/me/
# http://localhost/api/users/set_password/
router_v1.register(r'users', CustomUserViewSet, basename='custom-users')


authorization = [
    # Обрабатывает запросы на создание токена доступа
    # при входе пользователя в систему
    path(
        'auth/token/login/',
        views.TokenCreateView.as_view(),
        name='get_jwt_token'
    ),
    # Обрабатывает запросы на удаление (завершение) токена доступа
    # при выходе пользователя из системы
    path(
        'auth/token/logout/',
        views.TokenDestroyView.as_view(),
        name='delete_jwt_token'
    )
]

urlpatterns = [
    path('', include(authorization)),
    path('', include(router_v1.urls)),
    # Обрабатывает запросы на получение подписок
    path(
        'users/subscriptions/',
        CustomUserViewSet.as_view({'get': 'subscriptions'}),
        name='user-subscriptions'
    ),
    # Обрабатывает запросы на подписку и отписку от пользователя
    path(
        'users/<int:pk>/subscribe/',
        CustomUserViewSet.as_view({'get': 'subscribe', 'delete': 'subscribe'}),
        name='user-subscribe'
    ),
]
