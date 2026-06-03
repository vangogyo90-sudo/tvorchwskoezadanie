from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from .forms import CatForm
from .models import Cat
from .permissions import IsOwner
from .serializers import CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    serializer_class = CatSerializer
    permission_classes = (IsOwner,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("sex", "breed", "owner__username")
    search_fields = ("name", "breed", "color")
    ordering_fields = ("name", "birth_date", "created_at")

    class StandardResultsSetPagination(PageNumberPagination):
        page_size = 10

    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cat.objects.none()
        # If the request is anonymous, return empty queryset to avoid
        # attempting to compare AnonymousUser against FK fields.
        user = getattr(self.request, "user", None)
        if not (user and user.is_authenticated):
            return Cat.objects.none()
        # staff users can see all cats, regular users only their own
        if user.is_staff:
            return Cat.objects.select_related("owner").all()
        return Cat.objects.filter(owner=user)


# Frontend views for a simple "Kittygram"-style UI
def feed(request):
    """Show a simple feed of cats (public)."""
    cats = Cat.objects.select_related("owner").order_by("-created_at")[:50]
    return render(request, "cats/feed.html", {"cats": cats})


def cat_detail(request, pk):
    cat = get_object_or_404(Cat.objects.select_related("owner"), pk=pk)
    return render(request, "cats/cat_detail.html", {"cat": cat})


@login_required
def add_cat(request):
    if request.method == "POST":
        form = CatForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.owner = request.user
            cat.save()
            return redirect("feed")
    else:
        form = CatForm()
    return render(request, "cats/add_cat.html", {"form": form})

# Create your views here.
