from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path(
        'redoc/openapi-schema.yml',
        TemplateView.as_view(template_name='openapi-schema.yml'),
        name='redoc-schema'
    ),
    path('api/', include('users.urls')),
    path('api/', include('ingredients.urls')),
    path('api/', include('recipes.urls')),
]
