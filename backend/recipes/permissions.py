from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """Метод проверяет, является ли запрос
        методом безопасного доступа (GET)
        или аутентифицирован ли пользователь.
        """
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Метод проверяет, является ли запрос
        методом безопасного доступа (GET)
        или является ли пользователь автором объекта.
        """
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author)
