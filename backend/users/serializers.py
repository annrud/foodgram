from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe
from .models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для представления пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_is_subscribed(self, obj):
        """Метод определяет подписан ли текущий пользователь на объект User."""
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            subscriber=user,
            subscription=obj
        ).exists()


class RecipeUserSerializer(serializers.ModelSerializer):
    """Сериализатор для представления рецепта."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для представления данных о подписке."""
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
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
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
            if attrs['subscriber'] == attrs['subscription']:
                raise serializers.ValidationError(
                    'Нельзя подписываться на самого себя!'
                )
            if Subscription.objects.filter(
                    subscriber=attrs['subscriber'],
                    subscription=attrs['subscription']
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого автора!'
                )
        if (
                self.context['request'].method == 'DELETE'
                and not Subscription.objects.filter(
                    subscriber=attrs['subscriber'],
                    subscription=attrs['subscription']).exists()):
            raise serializers.ValidationError(
                'Вы не подписаны на этого автора!'
            )
        return attrs
