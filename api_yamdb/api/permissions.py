from rest_framework import permissions

class AuthorOrModeratorOrAdminOrReadonly(permissions.BasePermission):
    