from django.urls import include, path
from djoser import views
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router_v1 = DefaultRouter()

router_v1.register(r'users', CustomUserViewSet, basename='custom-users')


authorization = [
    path(
        'auth/token/login/',
        views.TokenCreateView.as_view(),
        name='get_auth_token'
    ),
    path(
        'auth/token/logout/',
        views.TokenDestroyView.as_view(),
        name='delete_auth_token'
    )
]

urlpatterns = [
    path('', include(authorization)),
    path('', include(router_v1.urls)),
    path(
        'users/subscriptions/',
        CustomUserViewSet.as_view({'get': 'subscriptions'}),
        name='user-subscriptions'
    ),
    path(
        'users/<int:pk>/subscribe/',
        CustomUserViewSet.as_view({'get': 'subscribe', 'delete': 'subscribe'}),
        name='user-subscribe'
    ),
]
