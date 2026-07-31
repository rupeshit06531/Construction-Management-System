from rest_framework import serializers

from .models import Payroll


class PayrollSerializer(serializers.ModelSerializer):

    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Payroll

        fields = [
            "id",
            "employee",
            "employee_name",
            "month",
            "basic_salary",
            "bonus",
            "deduction",
            "net_salary",
            "status",
            "payment_date",
            "remarks",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"