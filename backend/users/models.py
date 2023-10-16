from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint


class User(AbstractUser):
    # Поле для хранения электронной почты пользователя
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='e-mail'
    )
    # Поле для хранения имени пользователя (логина)
    username = models.CharField(
        max_length=150,
        verbose_name='Логин'
    )
    # Поле для хранения имени пользователя
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    # Поле для хранения фамилии пользователя
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    # Поле для хранения пароля пользователя
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль'
    )
    # Поле, используемое для аутентификации пользователя, - email
    USERNAME_FIELD = 'email'
    # Список полей, которые требуется указать при создании пользователя,
    # помимо обязательных полей (например, пароля)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Внутренний класс, содержащий дополнительные метаданные модели,
    # такие как порядок сортировки, а также "человекочитаемые" имена.
    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # Строковое представление экземпляра этого класса
    def __str__(self):
        return self.get_full_name()


class Subscription(models.Model):
    """Модель подписки на автора рецепта."""
    # Поле связывает каждую подписку с пользователем,
    # который подписывается
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписчик'
    )
    # Поле связывает каждую подписку с пользователем-автором рецепта
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Автор рецепта'
    )

    class Meta:
        constraints = [
            # Один пользователь не может подписаться
            # на одного и того же автора несколько раз
            UniqueConstraint(
                fields=['subscriber', 'subscription'],
                name='unique_subscriber_subscription'
            ),
            # Предотвращает попытку подписаться на самого себя,
            # так как автор и подписчик должны быть разными пользователями
            CheckConstraint(
                check=~Q(subscriber=F('subscription')),
                name='subscribe_to_yourself'
            ),
        ]
        # Человекочитаемые названия для модели и её множественной формы
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    # Cтроковое представление объекта Subscription,
    # вида "Пользователь подписан на Автор рецепта"
    def __str__(self):
        return f'{self.subscriber} подписан(а) на {self.subscription}'
