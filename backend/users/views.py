from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription
from .serializers import SubscriptionSerializer, UserSerializer

User = get_user_model()


class CustomUserViewSet(
    UserViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(
        detail=False, methods=['get'],
        queryset=Subscription.objects.all(),
        serializer_class=SubscriptionSerializer
    )
    def subscriptions(self, request):
        """Метод, который позволяет получить все подписки
        текущего пользователя.
        """
        user = self.request.user
        subscriptions = self.paginate_queryset(
            Subscription.objects.filter(subscriber=user)
        )
        serializer = self.get_serializer(subscriptions, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True, methods=['get', 'delete'],
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        """Метод, который обрабатывает запросы на подписку
         и отписку от пользователя.
         """
        user = self.request.user
        subscription_user = self.get_object()
        subscription_serializer = SubscriptionSerializer(
            context={
                'request': request
            },
            data={
                'subscriber': user.id,
                'subscription': subscription_user.id
            }
        )
        subscription_serializer.is_valid(raise_exception=True)
        if request.method == 'GET':
            subscription = Subscription.objects.create(
                subscriber=user, subscription=subscription_user
            )
            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscription, subscriber=user, subscription=subscription_user
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
