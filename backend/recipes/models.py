from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model

from ingredients.models import Ingredient

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название времени приёма пищи'
    )
    # Хранение цвета в формате HEX(например, "#FF0000")
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет в HEX'
    )
    # Короткий текстовый идентификатор для каждого тега
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    # Теги будут отсортированы по возрастанию идентификатора
    # Определено человекочитаемое имя для модели в
    # единственном и множественном числе
    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    # Строковое представление объекта
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    # Поле связывает рецепт с автором (пользователем).
    # При удалении автора, связанные рецепты также удаляются.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    # Поле связывает рецепт с ингредиентами через модель Amount.
    # Параметр related_name позволяет обратно связать рецепты с ингредиентами.
    # Через это поле можно получить список ингредиентов, необходимых для рецепта.
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Amount',
        related_name='recipes',
        verbose_name='Список ингредиентов',
    )
    # Поле связывает рецепт с тегами.
    # Параметр related_name позволяет обратно связать рецепты с тегами.
    # Через это поле можно получить список тегов, связанных с рецептом.
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список id тегов',
    )
    # Позволяет загружать изображение для рецепта.
    # Загруженное изображение будет сохранено в папке 'recipes/'.
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField(verbose_name='Описание')
    # Хранение времени приготовления.
    # Валидатор проверяет значение,
    # которое должно быть больше или равно 1 минуте.
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления не может быть менее 1 минуты.'
            )
        ],
        verbose_name='Время приготовления в минутах')
    # Поле автоматически заполняется датой и временем создания рецепта.
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        # Определено ограничение уникальности для пары
        # полей author и name, чтобы у каждого автора
        # не могло быть двух рецептов с одним и тем же названием.
        constraints = [
            UniqueConstraint(
                fields=['author', 'name'],
                name='unique_author_recipe'
            ),
        ]
        # Рецепты сортируются в обратном порядке по полю pub_date,
        # чтобы новые рецепты отображались первыми.
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    # Строковое представление объекта Recipe
    def __str__(self):
        return self.name


class Amount(models.Model):
    """
    Промежуточная модель между моделями Ингредиент и Рецепт,
    содержащая поле с количеством ингредиента.
    """
    # Поле связывает объект Amount с рецептом.
    # При удалении рецепта, все связанные объекты Amount также удаляются.
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_ingredients'
    )
    # Поле связывает объект Amount с ингредиентом.
    # При удалении ингредиента, все связанные объекты Amount также удаляются.
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_ingredients'
    )
    # Хранение количества ингредиента.
    # Есть валидатор, который проверяет, что значение больше или равно 1.
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиента'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    # Cтроковое представление объекта Amount,
    # которое включает название рецепта,
    # название ингредиента и количество с указанием
    # единицы измерения ингредиента.
    def __str__(self):
        return (
            f'{self.recipe.name}: {self.ingredient.name} '
            f'{self.amount}{self.ingredient.measurement_unit}.'
        )


class Purchase(models.Model):
    """Модель покупки."""
    # Поле связывает каждую покупку с пользователем,
    # при удалении пользователя также будут удалены
    # все связанные с ним покупки.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Покупатель'
    )
    # Поле связывает каждую покупку с рецептом
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Рецепты',
    )

    class Meta:
        # Гарантия уникальности комбинации user и recipe,
        # то есть пользователь не может добавить один
        # и тот же рецепт в покупку несколько раз.
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchase'
            )
        ]
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    #  Cтроковое представление объекта Purchase,
    #  Имя пользователя - Название рецепта
    def __str__(self):
        return (
            f'{self.user.username} - {self.recipe.name}'
        )


class Favorite(models.Model):
    """Модель избранных рецептов."""
    # Поле связывает каждый избранный рецепт с пользователем,
    # при удалении пользователя также будут удалены
    # все связанные с ним избранные рецепты
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    # Поле связывает каждый избранный рецепт с рецептом
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепты',
    )

    class Meta:
        # Один и тот же рецепт не может быть добавлен
        # в избранное пользователем несколько раз
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    #  Cтроковое представление объекта Favorite,
    #  Имя пользователя - Название рецепта
    def __str__(self):
        return (
            f'{self.user.username} - {self.recipe.name}'
        )
