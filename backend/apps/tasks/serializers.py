from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    project_name = serializers.CharField(
        source="project.name",
        read_only=True,
    )

    assigned_to_name = serializers.CharField(
        source="assigned_to.user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "project_name",
            "assigned_to",
            "assigned_to_name",
            "title",
            "description",
            "priority",
            "status",
            "start_date",
            "end_date",
            "completion_percentage",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "project_name",
            "assigned_to_name",
            "created_at",
            "updated_at",
        ]