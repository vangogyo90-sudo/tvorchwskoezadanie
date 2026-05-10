from rest_framework import serializers

from .models import Cat


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cat
        fields = (
            "id",
            "owner",
            "name",
            "birth_date",
            "sex",
            "breed",
            "color",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data):
        return Cat.objects.create(owner=self.context["request"].user, **validated_data)
