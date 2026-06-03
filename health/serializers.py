from rest_framework import serializers

from .models import Clinic, Doctor, HealthPassport, HealthRecord


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ("id", "name", "address", "phone")

    def validate_phone(self, value):
        if value:
            # simple validation: allow digits, spaces, +, -, parentheses
            import re
            if not re.match(r'^[0-9\s\-\+\(\)]+$', value):
                raise serializers.ValidationError("Invalid phone format")
        return value


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
    created_by = serializers.ReadOnlyField(source='created_by.username')

    next_due_date = serializers.DateField(required=False, allow_null=True)
    is_completed = serializers.BooleanField(required=False)

    class Meta:
        model = HealthRecord
        fields = ("id", "passport", "event_date", "next_due_date", "title", "description", "record_type", "clinic", "clinic_id", "doctor", "doctor_id", "created_by", "is_completed", "created_at")
        read_only_fields = ("created_at",)

    def validate(self, data):
        # Ensure next_due_date is not before event_date
        event = data.get('event_date')
        next_due = data.get('next_due_date')
        if event and next_due and next_due < event:
            raise serializers.ValidationError({'next_due_date': 'next_due_date must be >= event_date'})
        # Prevent duplicate record_type on same passport and date
        passport = data.get('passport')
        record_type = data.get('record_type')
        if passport and event and record_type:
            qs = HealthRecord.objects.filter(passport=passport, event_date=event, record_type=record_type)
            # when updating, exclude self (handled elsewhere)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError('A record of this type for the same date already exists for this passport')
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            validated_data['created_by'] = user
        return super().create(validated_data)


class HealthPassportSerializer(serializers.ModelSerializer):
    cat_name = serializers.ReadOnlyField(source='cat.name')
    records_total = serializers.IntegerField(source='records.count', read_only=True)

    class Meta:
        model = HealthPassport
        fields = ("id", "cat", "cat_name", "microchip_number", "blood_type", "weight_kg", "veterinarian_name", "created_at", "updated_at", "records_total")
        read_only_fields = ("created_at", "updated_at")
