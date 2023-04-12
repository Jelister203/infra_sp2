from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser


class AdminOrReadOnly(permissions.BasePermission):
    """
    Get method is available for all users,
    PATCH, DELETE - only for administrator
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in (
            'PATCH',
            'POST',
            'DELETE',
        ):
            return request.user.role == 'admin' or request.user.is_superuser
        return request.method == 'GET'


class IsModeratorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'moderator'


class IsUserWithPowerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ['admin', 'moderator']
        )
