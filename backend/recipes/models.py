from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model

from ingredients.models import Ingredient

User = get_user_model()


class Tag(models.Model):
    """Модель Тег."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название времени приёма пищи'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )
    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель Рецепт."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Amount',
        related_name='recipes',
        verbose_name='Список ингредиентов',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список id тегов',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления не может быть менее 1 минуты.'
            )
        ],
        verbose_name='Время приготовления в минутах')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'name'],
                name='unique_author_recipe'
            ),
        ]
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Amount(models.Model):
    """
    Модель Количество - промежуточная модель между
    моделями Ингредиент и Рецепт,
    содержащая поле с количеством ингредиента.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиента'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (
            f'{self.recipe.name}: {self.ingredient.name} '
            f'{self.amount}{self.ingredient.measurement_unit}.'
        )


class Purchase(models.Model):
    """Модель Покупка."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Рецепты',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchase'
            )
        ]
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return (
            f'{self.user.username} - {self.recipe.name}'
        )


class Favorite(models.Model):
    """Модель Избранный рецепт."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепты',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return (
            f'{self.user.username} - {self.recipe.name}'
        )
