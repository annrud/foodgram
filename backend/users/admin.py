from django.contrib import admin

from .models import Subscription, User

# Регистрирует модель Subscription для отображения в административной панели Django
admin.site.register(Subscription)

# Регистрирует кастомную конфигурацию для модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Список полей модели User, которые будут отображаться
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    # Поля, по которым можно выполнять поиск
    search_fields = ('username', 'email', 'first_name', )
    # Объекты User можно фильтровать по полям 'username' и 'email'
    list_filter = ('username', 'email', )

