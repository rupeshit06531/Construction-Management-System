from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):

    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance

        fields = [
            "id",
            "employee",
            "employee_name",
            "date",
            "status",
            "check_in",
            "check_out",
            "remarks",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]

    def get_employee_name(
        self,
        obj,
    ) -> str:
        return (
            f"{obj.employee.first_name} "
            f"{obj.employee.last_name}"
        )