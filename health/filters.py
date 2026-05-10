import django_filters

from .models import HealthPassport, HealthRecord


class HealthPassportFilter(django_filters.FilterSet):
    cat = django_filters.NumberFilter(field_name="cat_id")
    has_microchip = django_filters.BooleanFilter(method="filter_has_microchip")

    class Meta:
        model = HealthPassport
        fields = ("cat", "blood_type", "sterilized", "has_microchip")

    def filter_has_microchip(self, queryset, name, value):
        if value:
            return queryset.exclude(microchip_number="")
        return queryset.filter(microchip_number="")


class HealthRecordFilter(django_filters.FilterSet):
    cat = django_filters.NumberFilter(field_name="passport__cat_id")
    date_from = django_filters.DateFilter(field_name="event_date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="event_date", lookup_expr="lte")
    due_from = django_filters.DateFilter(field_name="next_due_date", lookup_expr="gte")
    due_to = django_filters.DateFilter(field_name="next_due_date", lookup_expr="lte")

    class Meta:
        model = HealthRecord
        fields = ("cat", "record_type", "date_from", "date_to", "due_from", "due_to")
