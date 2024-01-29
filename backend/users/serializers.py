from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe
from .models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для представления пользователя."""
    # Дополнительное поле будет отображать информацию о том,
    # подписан ли текущий пользователь на этого пользователя
    is_subscribed = serializers.SerializerMethodField()

    # Метаданные сериализатора
    class Meta:
        model = User
        # Поля модели User, включенные в сериализацию
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        # Поле password доступно только для записи,
        # оно не будет отображаться при сериализации
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_is_subscribed(self, obj):
        """Метод определяет подписан ли текущий пользователь на объект User."""
        # Определение текущего пользователя
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        # Проверка наличия подписки на заданного пользователя obj
        return Subscription.objects.filter(
            subscriber=user,
            subscription=obj
        ).exists()


class RecipeUserSerializer(serializers.ModelSerializer):
    """Сериализатор для представления рецепта."""
    class Meta:
        model = Recipe
        # Список полей модели Recipe,
        # которые должны быть включены в сериализованный вывод
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для представления данных о подписке."""
    # Поля email, id, username, first_name, last_name
    # берутся из связанного объекта subscription
    email = serializers.EmailField(read_only=True, source='subscription.email')
    id = serializers.IntegerField(read_only=True, source='subscription.id')
    username = serializers.CharField(
        read_only=True, source='subscription.username'
    )
    first_name = serializers.CharField(
        read_only=True, source='subscription.first_name'
    )
    last_name = serializers.CharField(
        read_only=True, source='subscription.last_name'
    )
    # Поля, определенные через SerializerMethodField вызывают
    # соответствующие методы get_is_subscribed, get_recipes, и get_recipes_count
    # Подписан ли пользователь на автора
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    # Рецепты автора
    recipes = serializers.SerializerMethodField(read_only=True)
    # Количество рецептов у автора
    recipes_count = serializers.SerializerMethodField(read_only=True)
    # Поля, которые используются для передачи идентификаторов
    # подписчика и автора, когда клиент делает запросы.
    # Они помечены как write_only, так как они не должны
    # быть отображены при сериализации,
    # но должны быть учтены во входных данных
    subscriber = serializers.IntegerField(write_only=True)
    subscription = serializers.IntegerField(write_only=True)

    class Meta:
        model = Subscription
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'subscriber',
            'subscription',
        ]

    def get_is_subscribed(self, obj):
        """Метод определяет подписан ли текущий
        пользователь на объект User.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            subscriber=user,
            subscription=obj.subscription
        ).exists()

    def get_recipes(self, obj):
        """Метод возвращает рецепты автора."""
        recipes = obj.subscription.recipes.all()
        return RecipeUserSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Метод возвращает количество рецептов автора."""
        return obj.subscription.recipes.count()

    def validate(self, attrs):
        """Проверка данных, полученных из запроса."""
        if self.context['request'].method == 'GET':
            # Проверка того, что пользователь не подписывается сам на себя
            if attrs['subscriber'] == attrs['subscription']:
                raise serializers.ValidationError(
                    'Нельзя подписываться на самого себя!'
                )
            # Проверка существования подписки на автора
            if Subscription.objects.filter(
                    subscriber=attrs['subscriber'],
                    subscription=attrs['subscription']
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого автора!'
                )
        if (
            # Проверка возможности отписки от автора
                self.context['request'].method == 'DELETE'
                and not Subscription.objects.filter(
                    subscriber=attrs['subscriber'],
                    subscription=attrs['subscription']).exists()):
            raise serializers.ValidationError(
                'Вы не подписаны на этого автора!'
            )
        return attrs
