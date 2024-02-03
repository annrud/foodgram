from django.contrib import admin

from .models import Amount, Favorite, Purchase, Recipe, Tag

admin.site.register(Amount)
admin.site.register(Favorite)
admin.site.register(Purchase)

# Инлайн-редактор для модели Amount,
# промежуточной таблицы,
# представляющей связь между Recipe и Ingredient
class AmountInline(admin.TabularInline):
    model = Recipe.ingredients.through
    # будет отображена одна дополнительная
    # форма для связанных объектов
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Поля для отображения, поиска и фильтрации
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # Указывем инлайн-редактор
    inlines = (AmountInline, )
    list_display = (
        'name',
        'author',
        'count_favorites'
    )
    # Поля для множественного выбора
    filter_horizontal = ('tags',)
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')

    # Метод для отображения количества добавлений в избранное
    @admin.display(description='добавлений в избранное')
    def count_favorites(self, recipe):
        return recipe.favorites.count()
