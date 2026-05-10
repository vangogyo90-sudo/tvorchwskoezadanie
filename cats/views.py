from rest_framework import viewsets

from accounts.models import Profile
from accounts.permissions import user_role

from .models import Cat
from .permissions import IsOwner
from .serializers import CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    serializer_class = CatSerializer
    permission_classes = (IsOwner,)
    search_fields = ("name", "breed", "color")
    ordering_fields = ("name", "birth_date", "created_at")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cat.objects.none()
        if user_role(self.request.user) in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
            return Cat.objects.select_related("owner")
        return Cat.objects.filter(owner=self.request.user)

# Create your views here.
