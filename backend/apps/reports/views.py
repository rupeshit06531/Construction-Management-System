from django.db.models import Sum

from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from apps.accounts.permissions import IsAdminManagerEngineer
from apps.common.mixins import RolePermissionMixin
from apps.employees.models import Employee
from apps.expenses.models import Expense
from apps.payroll.models import Payroll
from apps.projects.models import Project

from .models import Report
from .serializers import ReportSerializer


class DashboardReportItemSerializer(serializers.Serializer):
    title = serializers.CharField()
    total = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        required=False,
    )


@extend_schema(
    tags=["Reports"],
    summary="Dashboard report",
    description=(
        "Returns summary report data including projects, "
        "employees, expenses and payroll statistics."
    ),
    responses=DashboardReportItemSerializer(many=True),
)
class DashboardReportAPIView(
    RolePermissionMixin,
    APIView,
):
    role_permissions = {
        "GET": IsAdminManagerEngineer,
    }

    def get(self, request):
        total_expenses = (
            Expense.objects.aggregate(
                total=Sum("amount"),
            )["total"]
            or 0
        )

        data = [
            {
                "title": "Total Projects",
                "total": Project.objects.count(),
            },
            {
                "title": "Total Employees",
                "total": Employee.objects.count(),
            },
            {
                "title": "Total Expenses",
                "amount": total_expenses,
            },
            {
                "title": "Total Payroll Records",
                "total": Payroll.objects.count(),
            },
        ]

        serializer = DashboardReportItemSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)


@extend_schema(
    tags=["Reports"],
    summary="List and create reports",
)
class ReportListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):
    queryset = Report.objects.select_related(
        "generated_by",
    ).all()

    serializer_class = ReportSerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "POST": IsAdminManagerEngineer,
    }

    def perform_create(self, serializer):
        serializer.save(
            generated_by=self.request.user,
        )


@extend_schema(
    tags=["Reports"],
    summary="Retrieve, update or delete report",
)
class ReportDetailAPIView(
    RolePermissionMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = Report.objects.select_related(
        "generated_by",
    ).all()

    serializer_class = ReportSerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "PUT": IsAdminManagerEngineer,
        "PATCH": IsAdminManagerEngineer,
        "DELETE": IsAdminManagerEngineer,
    }