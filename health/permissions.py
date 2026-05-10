from rest_framework import permissions

from accounts.models import Profile
from accounts.permissions import user_role


class IsPassportOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        role = user_role(request.user)
        if role in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if user_role(request.user) in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
            return True
        if hasattr(obj, "cat"):
            return obj.cat.owner == request.user
        return obj.passport.cat.owner == request.user
