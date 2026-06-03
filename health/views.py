from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import HealthPassport, HealthRecord, Clinic, Doctor
from .permissions import IsPassportOwner
from .serializers import HealthPassportSerializer, HealthRecordSerializer, ClinicSerializer, DoctorSerializer
import django_filters


class HealthRecordFilter(django_filters.FilterSet):
    event_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = HealthRecord
        fields = {
            'record_type': ['exact'],
            'passport__cat__name': ['icontains'],
            'event_date': ['exact', 'gte', 'lte'],
        }


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10


class HealthPassportViewSet(viewsets.ModelViewSet):
    serializer_class = HealthPassportSerializer
    queryset = HealthPassport.objects.select_related('cat')
    permission_classes = (IsPassportOwner,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("cat__name", "microchip_number", "blood_type", "cat__owner__username")
    search_fields = ("cat__name", "microchip_number")
    ordering_fields = ("created_at",)
    pagination_class = StandardResultsSetPagination


class HealthRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    queryset = HealthRecord.objects.select_related('passport', 'passport__cat')
    permission_classes = (IsPassportOwner,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = HealthRecordFilter
    search_fields = ("notes",)
    ordering_fields = ("event_date",)
    # Default list() will be unpaginated; provide separate actions for paginated and search

    @action(detail=False, methods=["get"], url_path="paginated")
    def paginated(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ClinicViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "address")
    ordering_fields = ("name",)
    pagination_class = StandardResultsSetPagination


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.select_related('clinic')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "specialization")
    ordering_fields = ("name",)
    pagination_class = StandardResultsSetPagination
