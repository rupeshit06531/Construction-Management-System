from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(
        source="manager.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "code",
            "description",
            "client",
            "location",
            "start_date",
            "end_date",
            "budget",
            "status",
            "manager",
            "manager_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "manager_name",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None),
        )
        end_date = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None),
        )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {
                    "end_date": (
                        "End date cannot be earlier than start date."
                    )
                }
            )

        return attrs