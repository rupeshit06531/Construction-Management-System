from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):

    project_name = serializers.CharField(
        source="project.name",
        read_only=True,
    )

    class Meta:
        model = Expense

        fields = [
            "id",
            "project",
            "project_name",
            "title",
            "category",
            "amount",
            "expense_date",
            "description",
            "created_at",
            "updated_at",
        ]