from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from accounts.models import Profile
from accounts.permissions import user_role
from cats.models import Cat
from cats.serializers import CatSerializer

from .models import HealthPassport, HealthRecord


class CatBriefSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class HealthRecordSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    passport_id = serializers.PrimaryKeyRelatedField(
        queryset=HealthPassport.objects.none(),
        source="passport",
        write_only=True,
    )
    cat = serializers.SerializerMethodField()

    class Meta:
        model = HealthRecord
        fields = (
            "id",
            "passport_id",
            "cat",
            "created_by",
            "record_type",
            "title",
            "event_date",
            "next_due_date",
            "clinic",
            "doctor",
            "weight_kg",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            if user_role(request.user) in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
                self.fields["passport_id"].queryset = HealthPassport.objects.all()
            else:
                self.fields["passport_id"].queryset = HealthPassport.objects.filter(cat__owner=request.user)

    @extend_schema_field(CatBriefSerializer)
    def get_cat(self, obj):
        return {"id": obj.passport.cat_id, "name": obj.passport.cat.name}

    def validate(self, attrs):
        event_date = attrs.get("event_date", getattr(self.instance, "event_date", None))
        next_due_date = attrs.get("next_due_date", getattr(self.instance, "next_due_date", None))
        if event_date and next_due_date and next_due_date < event_date:
            raise serializers.ValidationError({"next_due_date": "Следующий срок не может быть раньше даты события."})
        return attrs

    def create(self, validated_data):
        return HealthRecord.objects.create(created_by=self.context["request"].user, **validated_data)


class HealthPassportSerializer(serializers.ModelSerializer):
    cat = CatSerializer(read_only=True)
    cat_id = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.none(), source="cat", write_only=True)
    records_count = serializers.IntegerField(read_only=True)
    upcoming_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = HealthPassport
        fields = (
            "id",
            "cat",
            "cat_id",
            "microchip_number",
            "blood_type",
            "sterilized",
            "weight_kg",
            "allergies",
            "chronic_conditions",
            "veterinarian_name",
            "clinic_phone",
            "emergency_notes",
            "records_count",
            "upcoming_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            if user_role(request.user) in (Profile.ROLE_ADMIN, Profile.ROLE_VETERINARIAN):
                queryset = Cat.objects.all()
            else:
                queryset = Cat.objects.filter(owner=request.user)
            if self.instance is None:
                queryset = queryset.filter(health_passport__isnull=True)
            self.fields["cat_id"].queryset = queryset

    def validate_cat(self, cat):
        if self.instance is None and hasattr(cat, "health_passport"):
            raise serializers.ValidationError("Для этого кота уже создан паспорт здоровья.")
        return cat
