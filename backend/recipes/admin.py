from django.contrib import admin

from .models import Amount, Favorite, Purchase, Recipe, Tag

admin.site.register(Amount)
admin.site.register(Favorite)
admin.site.register(Purchase)


class AmountInline(admin.TabularInline):
    """
    Инлайн-редактор для модели Amount,
    промежуточной таблицы, представляющей связь
    между Recipe и Ingredient.
    """
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Класс для отображения модели Tag в админ-панели."""
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс для отображения модели Recipe в админ-панели."""
    inlines = (AmountInline, )
    list_display = (
        'name',
        'author',
        'count_favorites'
    )
    filter_horizontal = ('tags',)
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')

    @admin.display(description='добавлений в избранное')
    def count_favorites(self, recipe):
        """Метод для отображения количества добавлений в избранное."""
        return recipe.favorites.count()
