from rest_framework import permissions

from .models import Profile


def user_role(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser or user.is_staff:
        return Profile.ROLE_ADMIN
    return getattr(getattr(user, "profile", None), "role", Profile.ROLE_OWNER)


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_role(request.user) == Profile.ROLE_ADMIN
