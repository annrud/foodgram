from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ingredients.models import Ingredient
from users.serializers import UserSerializer
from .models import Amount, Favorite, Purchase, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для представления тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class AmountSerializer(serializers.ModelSerializer):
    """Сериализатор для представления ингредиентов и их количестве."""
    # идентификатор ингредиента берем из поля id модели ingredient
    id = serializers.IntegerField(source='ingredient.id')
    # Имя ингредиента берем из поля name модели ingredient
    name = serializers.CharField(source='ingredient.name')
    # Единица измерения ингредиента
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о рецептах."""
    # Список тегов
    tags = TagSerializer(many=True, read_only=True)
    # Автор рецепта
    author = UserSerializer(read_only=True)
    # список ингредиентов рецепта
    ingredients = AmountSerializer(
        many=True, read_only=True, source='amount_ingredients'
    )
    # Поле для указания, добавлен ли рецепт в избранное текущим пользователем
    is_favorited = SerializerMethodField()
    # Поле для указания, добавлен ли рецепт в корзину покупок текущим пользователем
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        # Поля, которые будут включены в сериализацию
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        """Получение значения поля is_favorited."""
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Получение значения поля is_in_shopping_cart."""
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Purchase.objects.filter(user=user, recipe=obj).exists()

    def to_representation(self, obj):
        """Переопределённый метод для включения URL изображения в выходные данные."""
        response = super(
            RecipeReadSerializer,
            self
        ).to_representation(obj)
        # Проверка наличия изображения в объекте instance
        if obj.image:
            # добавление в ответ поля 'image' с URL изображения
            response['image'] = obj.image.url
        return response


class AmountCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта модели Amount,
    включающий в себя идентификатор ингредиента и его количество."""
    # Идентификатор ингредиента, устанавливается флаг write_only=True,
    # потому что это поле нужно только при создании нового объекта Amount,
    # и не должно включаться в представление при выводе (сериализации).
    id = serializers.IntegerField(write_only=True)
    # Указание количества ингредиента в рецепте
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = Amount
        fields = ('id', 'amount')


class RecipeChangeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления рецептов."""
    # Список идентификаторов ингредиентов и их количеств
    ingredients = AmountCreateSerializer(many=True)
    # Изображение в формате base64
    image = Base64ImageField(max_length=False, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def validate(self, attrs):
        """Метод, который валидирует данные перед созданием или обновлением рецепта."""
        # Проверка уникальности названия рецепта
        if self.context['request'].method == 'POST' and Recipe.objects.filter(
                author=self.context['request'].user, name=attrs['name']
        ).exists():
            raise serializers.ValidationError(
                'Вы уже создавали такой рецепт!')
        # Проверка положительности времени приготовления
        if attrs['cooking_time'] <= 0:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше или равно нулю!'
            )
        tags = attrs['tags']
        tags_list = []
        # Проверка уникальности тегов
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Теги не должны повторяться!'
                )
            tags_list.append(tag)
        ingredients = attrs['ingredients']
        ingredients_list = []
        # Проверка уникальности ингредиентов
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться!'
                )
            # Проверка положительности количества ингредиента
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиентов '
                    'не должно быть меньше или равно нулю!'
                )
            ingredients_list.append(ingredient['id'])
        return attrs

    def add_ingredient_to_recipe(self, recipe, ingredients):
        """Метод добавления ингредиента в рецепт."""
        for ingredient in ingredients:
            ingredient_object = get_object_or_404(
                Ingredient, id=ingredient['id']
            )
            # through_defaults используется для передачи
            # дополнительных данных для связи многие ко многим
            recipe.ingredients.add(
                ingredient_object,
                through_defaults={'amount': ingredient['amount']}
            )

    def create(self, validated_data):
        """Метод создания рецепта на основе
        предоставленных валидированных данных.
        """
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        # Создание объекта рецепта, из validated_data
        # извлечены ingredients и tags,
        # автор рецепта - текущий пользователь
        recipe = Recipe.objects.create(
            **validated_data, author=self.context['request'].user
        )
        # Созданный рецепт связывается с тегами
        recipe.tags.add(*tags)
        # Добавление ингредиентов к рецепту
        self.add_ingredient_to_recipe(recipe, ingredients)
        # сохранение рецепта в базе данных
        recipe.save()
        return recipe

    def update(self, obj, validated_data):
        """Метод обновления рецепта на основе
        предоставленных валидированных данных."""
        # Извлечение ingredients и tags
        # из валидированных данных
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        # Очистка связанных полей у существующего рецепта
        obj.tags.clear()
        obj.ingredients.clear()
        # Добавляем новые теги и ингредиенты к рецепту
        obj.tags.add(*tags)
        self.add_ingredient_to_recipe(obj, ingredients)
        # Вызов родительского метода update для обновления
        # объекта существующего рецепта
        return super().update(obj, validated_data)

    def to_representation(self, obj):
        """Метод преобразует объект рецепта в представление
        RecipeReadSerializer, включающее теги и ингредиенты и др. в ответ.
        """
        return RecipeReadSerializer(obj, context=self.context).data


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого представления рецепта."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class PurchaseSerializer(serializers.ModelSerializer):
    """Сериализатор для представления списка покупок."""
    class Meta:
        # Модель для сериализации и поля,
        # которые будут включены в сериализованный вывод
        model = Purchase
        fields = ('user', 'recipe')

    def validate(self, attrs):
        """Валидация данных перед сохранением/удалением объекта."""
        # Проверка перед добавлением на наличие рецепта в списке покупок
        if self.context['request'].method == 'GET' and Purchase.objects.filter(
                user=attrs['user'], recipe=attrs['recipe']
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже есть в списке покупок!'
            )
        # Проверка наличия рецепта в списке покупок перед его удалением
        if (
                self.context['request'].method == 'DELETE'
                and not Purchase.objects.filter(
                user=attrs['user'], recipe=attrs['recipe']).exists()):
            raise serializers.ValidationError('Рецепта нет в списке покупок!')
        return attrs


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для представления списка избранных рецептов."""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, attrs):
        """Валидация данных перед сохранением/удалением объекта."""
        # Проверка перед добавлением на наличие рецепта в списке избранных рецептов
        if self.context['request'].method == 'GET' and Favorite.objects.filter(
                user=attrs['user'], recipe=attrs['recipe']
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже есть в списке избранных рецептов!'
            )
        # Проверка наличия рецепта в списке избранных рецептов перед его удалением
        if (
                self.context['request'].method == 'DELETE'
                and not Favorite.objects.filter(
                user=attrs['user'], recipe=attrs['recipe']).exists()):
            raise serializers.ValidationError(
                'Рецепта нет в списке избранных рецептов!'
            )
        return attrs
