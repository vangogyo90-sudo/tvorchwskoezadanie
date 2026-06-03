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


class IsOwnerCreatorOrModerator(permissions.BasePermission):
    """Permission where moderators (staff) have full access, owners (cat.owner) can manage objects for their pets,
    and creators (created_by) can edit their own created records. Others have read-only access.
    """
    def has_permission(self, request, view):
        # Allow any authenticated user to list/read; further checks in object permission
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # staff/moderator: full access
        if request.user and request.user.is_staff:
            return True
        # determine owner (cat.owner) for HealthRecord or HealthPassport
        owner = getattr(obj, 'cat', None) or getattr(getattr(obj, 'passport', None), 'cat', None)
        if owner and owner.owner == request.user:
            # owners can read and modify
            return True
        # creators can modify their own created objects
        creator = getattr(obj, 'created_by', None)
        if creator and creator == request.user:
            return True
        # otherwise allow safe methods only
        return request.method in permissions.SAFE_METHODS
