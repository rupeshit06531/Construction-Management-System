from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "report_type",
            "generated_by",
            "generated_by_name",
            "start_date",
            "end_date",
            "data",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "generated_by",
            "generated_by_name",
            "created_at",
            "updated_at",
        ]

    def get_generated_by_name(self, obj):
        if not obj.generated_by:
            return None

        full_name = obj.generated_by.get_full_name()

        return full_name or obj.generated_by.username