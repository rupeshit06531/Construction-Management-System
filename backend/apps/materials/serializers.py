from rest_framework import serializers

from .models import Material


class MaterialSerializer(serializers.ModelSerializer):

    project_name = serializers.CharField(
        source="project.name",
        read_only=True,
    )

    class Meta:
        model = Material

        fields = [
            "id",
            "project",
            "project_name",
            "name",
            "category",
            "unit",
            "quantity",
            "purchase_price",
            "supplier",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]