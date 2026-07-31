from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee

        fields = [
            "id",
            "first_name",
            "last_name",
            "employee_type",
            "phone",
            "email",
            "joining_date",
            "salary",
            "address",
            "created_at",
            "updated_at",
        ]