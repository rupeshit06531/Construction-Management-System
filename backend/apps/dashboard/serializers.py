from rest_framework import serializers


class DashboardKPISerializer(serializers.Serializer):
    total_projects = serializers.IntegerField()
    total_employees = serializers.IntegerField()
    total_tasks = serializers.IntegerField()
    total_materials = serializers.IntegerField()
    total_inventory_items = serializers.IntegerField()
    total_expenses = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
    )
    total_payroll = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

class MonthlyExpenseSerializer(serializers.Serializer):
    month = serializers.CharField()
    total_expense = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
    )


class MonthlyPayrollSerializer(serializers.Serializer):
    month = serializers.CharField()
    total_payroll = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
    )


class ProjectStatusSerializer(serializers.Serializer):
    status = serializers.CharField()
    total = serializers.IntegerField()