from rest_framework import serializers

from .models import HealthPassport, HealthRecord, Clinic, Doctor


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ("id", "name", "address", "phone")


class DoctorSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    clinic_id = serializers.PrimaryKeyRelatedField(queryset=Clinic.objects.all(), source='clinic', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Doctor
        fields = ("id", "name", "specialization", "clinic", "clinic_id")


class HealthRecordSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    clinic_id = serializers.PrimaryKeyRelatedField(queryset=Clinic.objects.all(), source='clinic', write_only=True, required=False, allow_null=True)
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), source='doctor', write_only=True, required=False, allow_null=True)

    class Meta:
        model = HealthRecord
        fields = ("id", "passport", "event_date", "title", "description", "record_type", "clinic", "clinic_id", "doctor", "doctor_id", "created_at")
        read_only_fields = ("created_at",)


class HealthPassportSerializer(serializers.ModelSerializer):
    cat_name = serializers.ReadOnlyField(source='cat.name')
    records_total = serializers.IntegerField(source='records.count', read_only=True)

    class Meta:
        model = HealthPassport
        fields = ("id", "cat", "cat_name", "microchip_number", "blood_type", "weight_kg", "veterinarian_name", "created_at", "updated_at", "records_total")
        read_only_fields = ("created_at", "updated_at")
