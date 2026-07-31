from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    project_name = serializers.CharField(
        source="project.name",
        read_only=True
    )

    assigned_employee_name = serializers.SerializerMethodField()


    class Meta:
        model = Task

        fields = [
            "id",
            "title",
            "description",
            "project",
            "project_name",
            "assigned_to",
            "assigned_employee_name",
            "priority",
            "status",
            "start_date",
            "end_date",
            "completion_percentage",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]


    def get_assigned_employee_name(self, obj):

        if obj.assigned_to:
            return (
                f"{obj.assigned_to.first_name} "
                f"{obj.assigned_to.last_name}"
            )

        return None