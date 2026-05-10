from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import Profile
from accounts.permissions import user_role

from .filters import HealthPassportFilter, HealthRecordFilter
from .models import HealthPassport, HealthRecord
from .permissions import IsPassportOwner
from .serializers import HealthPassportSerializer, HealthRecordSerializer


class HealthPassportViewSet(viewsets.ModelViewSet):
    serializer_class = HealthPassportSerializer
    permission_classes = (IsPassportOwner,)
    filterset_class = HealthPassportFilter
    search_fields = ("cat__name", "microchip_number", "veterinarian_name")
    ordering_fields = ("cat__name", "updated_at", "weight_kg")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return HealthPassport.objects.none()
        if user_role(self.request.user) in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
            base_queryset = HealthPassport.objects.all()
        else:
            base_queryset = HealthPassport.objects.filter(cat__owner=self.request.user)
        return (
            base_queryset
            .select_related("cat", "cat__owner")
            .annotate(
                records_count=Count("records", distinct=True),
                upcoming_count=Count("records", filter=Q(records__next_due_date__gte=timezone.localdate()), distinct=True),
            )
        )

    @action(detail=False, methods=("get",), url_path="upcoming")
    def upcoming(self, request):
        records_queryset = HealthRecord.objects.filter(next_due_date__gte=timezone.localdate())
        if user_role(request.user) not in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
            records_queryset = records_queryset.filter(passport__cat__owner=request.user)
        records = (
            records_queryset
            .select_related("passport", "passport__cat", "created_by")
            .order_by("next_due_date", "passport__cat__name")
        )
        page = self.paginate_queryset(records)
        context = self.get_serializer_context()
        if page is not None:
            serializer = HealthRecordSerializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        serializer = HealthRecordSerializer(records, many=True, context=context)
        return Response(serializer.data)


class HealthRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    permission_classes = (IsPassportOwner,)
    filterset_class = HealthRecordFilter
    search_fields = ("title", "description", "clinic", "doctor", "passport__cat__name")
    ordering_fields = ("event_date", "next_due_date", "created_at")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return HealthRecord.objects.none()
        if user_role(self.request.user) in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
            base_queryset = HealthRecord.objects.all()
        else:
            base_queryset = HealthRecord.objects.filter(passport__cat__owner=self.request.user)
        return base_queryset.select_related(
            "passport",
            "passport__cat",
            "created_by",
        )

    @action(detail=False, methods=("get",), url_path="upcoming")
    def upcoming(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(next_due_date__gte=timezone.localdate()).order_by("next_due_date"))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Create your views here.
