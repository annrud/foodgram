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
    # Получаем всех пользователей
    queryset = User.objects.all()
    # Используем сериализатор UserSerializer
    serializer_class = UserSerializer
    # Атрибут, который определяет правила разрешений.
    # Здесь устанавливается правило, что пользователь
    # должен быть аутентифицирован для доступа к представлению.
    permission_classes = (permissions.IsAuthenticated,)

    # Декоратор, который добавляет новое действие к представлению.
    # В данном случае, это действие предназначено для обработки
    # HTTP GET запроса.
    # detail=False указывает, что это действие применяется
    # не к конкретному объекту, а к коллекции
    @action(
        detail=False, methods=['get'],
        queryset=Subscription.objects.all(),
        serializer_class=SubscriptionSerializer
    )
    def subscriptions(self, request):
        """Метод, который позволяет получить все подписки
        текущего пользователя.
        """
        # Извлечение текущего пользователя,
        # отправившего запрос, из объекта request
        user = self.request.user
        # Подписки текущего пользователя,
        # метод paginate_queryset используется
        # для разбиения результатов на страницы,
        # если список слишком большой
        subscriptions = self.paginate_queryset(
            Subscription.objects.filter(subscriber=user)
        )
        # Создание экземпляра сериализатора для проверки и
        # десериализация ввода и сериализация вывода
        # many=True указывает, что сериализуется не один объект, а список
        serializer = self.get_serializer(subscriptions, many=True)
        # Возвращаем сериализованные данные как ответ на запрос
        # с учётом пагинации, если она была применена
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True, methods=['get', 'delete'],
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        """Метод, который обрабатывает запросы на подписку
         и отписку от пользователя.
         """
        # Получение текущего аутентифицированного пользователя
        user = self.request.user
        # Получение объекта пользователя,
        # на который текущий пользователь желает подписаться
        subscription_user = self.get_object()
        # Создание экземпляра сериализатора
        # для создания или удаления подписки
        subscription_serializer = SubscriptionSerializer(
            context={
                'request': request
            },
            data={
                'subscriber': user.id,
                'subscription': subscription_user.id
            }
        )
        # Проверка валидности данных и генерация
        # исключения в случае ошибки валидации
        subscription_serializer.is_valid(raise_exception=True)
        if request.method == 'GET':
            # Создание новой подписки
            subscription = Subscription.objects.create(
                subscriber=user, subscription=subscription_user
            )
            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            # Удаление существующей подписки
            subscription = get_object_or_404(
                Subscription, subscriber=user, subscription=subscription_user
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
