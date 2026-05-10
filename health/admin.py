from django.contrib import admin

from .models import HealthPassport, HealthRecord


@admin.register(HealthPassport)
class HealthPassportAdmin(admin.ModelAdmin):
    list_display = ("cat", "microchip_number", "blood_type", "sterilized", "weight_kg", "updated_at")
    list_filter = ("blood_type", "sterilized", "updated_at")
    search_fields = ("cat__name", "microchip_number", "veterinarian_name", "clinic_phone")


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "passport", "record_type", "event_date", "next_due_date", "created_by")
    list_filter = ("record_type", "event_date", "next_due_date")
    search_fields = ("title", "description", "passport__cat__name", "clinic", "doctor")
    date_hierarchy = "event_date"

# Register your models here.
