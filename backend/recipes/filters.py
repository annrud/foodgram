from django_filters import rest_framework as filters

from .models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    # Этот фильтр позволит фильтровать рецепты,
    # чтобы получить только те, которые принадлежат
    # конкретному автору (пользователю) по его идентификатору id.
    # Например, запрос /?author=1
    author = filters.NumberFilter(
        # Поле модели, по которому будет происходить фильтрация
        # (поле id из связанной модели User)
        field_name='author__id',
        # Тип операции сравнения для фильтра - точное совпадение
        lookup_expr='exact'
    )
    # Фильтрация рецептов по нескольким тегам,
    # например, /?tags=tag1,tag2,tag3
    tags = filters.ModelMultipleChoiceFilter(
        # Здесь используется поле slug тега (расположено в связанной модели Tag)
        field_name='tags__slug',
        # Поле, которое будет использоваться для сравнения
        # с переданными значениями фильтра
        to_field_name='slug',
        # Набор данных, который будет использоваться для
        # получения возможных значений фильтра
        queryset=Tag.objects.all(),
        # Тип операции сравнения для фильтра
        # позволяет выбирать записи, у которых значение slag
        # совпадает хотя бы с одним из переданных значений
        # lookup_expr='in'
    )
    # Фильтр избранных рецептов, например,
    # передавая параметр is_favorited=true в URL,
    # фильтр вернет только те рецепты,
    # которые добавлены в избранное текущим пользователем
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    # Фильтр рецептов в списке покупок, например,
    # передавая параметр is_in_shopping_cart=true в URL,
    # фильтр вернет только те рецепты,
    # которые добавлены в список покупок текущим пользователем
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def filter_is_favorited(self, queryset, *args):
        """Фильтрует рецепты, которые были добавлены
        в избранное текущим пользователем.
        """
        return queryset.filter(favorites__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, *args):
        """Фильтрует рецепты, которые находятся
        в списке покупок текущего пользователя.
        """
        return queryset.filter(purchases__user=self.request.user)
