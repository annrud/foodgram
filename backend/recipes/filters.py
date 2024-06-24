from django_filters import rest_framework as filters

from .models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """
    Класс для фильтрации рецептов по идентификатору автора,
    по нескольким тегам, по добавлению в избранное и список покупок.
    """

    author = filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact'
    )

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
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
