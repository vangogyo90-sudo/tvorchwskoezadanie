from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Simple owner permission: staff users can manage all, others read-only except create."""
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS or request.method == "POST"

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS and obj.owner == request.user
