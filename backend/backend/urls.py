from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    # Этот путь связывает URL-адрес, оканчивающийся на "admin/",
    # с функциональностью административной панели Django.
    # Предоставляет доступ к администрированию приложения
    path("admin/", admin.site.urls),
    # Этот путь ассоциирует URL-адрес "redoc/" с классом TemplateView,
    # который используется для отображения статичных HTML-шаблонов
    # При обращении к "redoc/", будет отображаться HTML-шаблон из файла "redoc.html"
    # name='redoc' - задает имя пути
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    # Cвязывает URL "redoc/openapi-schema.yml" с классом TemplateView,
    # при обращении к нему будет отображаться HTML-шаблон из файла "openapi-schema.yml".
    path(
        'redoc/openapi-schema.yml',
        TemplateView.as_view(template_name='openapi-schema.yml'),
        name='redoc-schema'
    ),
    # URL-адреса, начинающиеся с "api/", будут передаваться
    # для обработки в модули urls.py приложений,
    # где они могут быть дополнительно маршрутизированы
    path('api/', include('users.urls')),
    path('api/', include('ingredients.urls')),
    path('api/', include('recipes.urls')),
]
