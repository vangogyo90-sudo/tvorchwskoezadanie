from rest_framework import permissions

from accounts.models import Profile
from accounts.permissions import user_role


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        role = user_role(request.user)
        if role in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
            return True
        return request.method in permissions.SAFE_METHODS or request.method == "POST"

    def has_object_permission(self, request, view, obj):
        if user_role(request.user) in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
            return True
        return request.method in permissions.SAFE_METHODS and obj.owner == request.user
