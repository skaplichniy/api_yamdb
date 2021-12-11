from rest_framework import permissions
from reviews.models import User


class AuthorOrModeratorOrAdminOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
                request.method in permissions.SAFE_METHODS
                or request.user
                and request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        return bool(
                request.method in permissions.SAFE_METHODS
                or request.user
                and request.user.is_authenticated
                and request.user == obj.author
                or request.user.role == User.MODERATOR
                or request.user.role == User.ADMIN
                or request.user.is_superuser
        )


class AdminOrReadonly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )


class SelfOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.ADMIN
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user == obj
            or request.user.role == User.ADMIN
            or request.user.is_superuser
        )

class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS