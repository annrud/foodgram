from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint


class User(AbstractUser):
    """Модель Пользователь."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='e-mail'
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Логин'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name()


class Subscription(models.Model):
    """Модель Подписка на автора рецепта."""
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписчик'
    )
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Автор рецепта'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['subscriber', 'subscription'],
                name='unique_subscriber_subscription'
            ),
            CheckConstraint(
                check=~Q(subscriber=F('subscription')),
                name='subscribe_to_yourself'
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.subscriber} подписан(а) на {self.subscription}'
