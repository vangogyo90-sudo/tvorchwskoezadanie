import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Clinic, Doctor, HealthPassport, HealthRecord, Vaccine, VaccineAdministration
from .permissions import IsPassportOwner
from .serializers import (ClinicSerializer, DoctorSerializer,
                          HealthPassportSerializer, HealthRecordSerializer,
                          VaccineSerializer, VaccineAdministrationSerializer)


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
    # Use standard DRF pagination/search on GET /api/health-passports/
    pagination_class = StandardResultsSetPagination


class HealthRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    queryset = HealthRecord.objects.select_related('passport', 'passport__cat')
    permission_classes = (IsPassportOwner,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = HealthRecordFilter
    search_fields = ("title", "description", "passport__cat__name", "doctor__name", "clinic__name")
    ordering_fields = ("event_date",)
    # Use standard DRF pagination/search on GET /api/health-records/
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        """POST: mark a HealthRecord as completed."""
        record = self.get_object()
        record.is_completed = True
        record.save()
        serializer = self.get_serializer(record)
        return Response(serializer.data)


class ClinicViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "address")
    ordering_fields = ("name",)
    # Use standard DRF pagination/search on GET /api/clinics/
    pagination_class = StandardResultsSetPagination


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.select_related('clinic')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "specialization")
    ordering_fields = ("name",)
    # Use standard DRF pagination/search on GET /api/doctors/
    pagination_class = StandardResultsSetPagination


class VaccineViewSet(viewsets.ModelViewSet):
    serializer_class = VaccineSerializer
    queryset = Vaccine.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "manufacturer")
    ordering_fields = ("name",)
    pagination_class = StandardResultsSetPagination


class VaccineAdministrationViewSet(viewsets.ModelViewSet):
    serializer_class = VaccineAdministrationSerializer
    queryset = VaccineAdministration.objects.select_related('vaccine', 'passport', 'doctor', 'clinic')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("vaccine__name", "passport__cat__name", "administered_at")
    search_fields = ("vaccine__name", "passport__cat__name")
    ordering_fields = ("administered_at",)
    pagination_class = StandardResultsSetPagination
