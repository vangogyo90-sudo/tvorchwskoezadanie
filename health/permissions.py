from rest_framework import permissions


class IsPassportOwner(permissions.BasePermission):
    """Allow staff full access; owners can view related passports/records and create records."""
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS or request.method == 'POST'

    def has_object_permission(self, request, view, obj):
        # obj can be HealthPassport or HealthRecord
        owner = getattr(obj, 'cat', None) or getattr(getattr(obj, 'passport', None), 'cat', None)
        if request.user and request.user.is_staff:
            return True
        if owner is None:
            return False
        return request.method in permissions.SAFE_METHODS and owner.owner == request.user
