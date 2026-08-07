from django.urls import path

from .views import (
    DashboardKPIAPIView,
    MonthlyExpenseAPIView,
    MonthlyPayrollAPIView,
)


urlpatterns = [
    path(
        "kpi/",
        DashboardKPIAPIView.as_view(),
        name="dashboard-kpi",
    ),
    path(
        "monthly-expenses/",
        MonthlyExpenseAPIView.as_view(),
        name="monthly-expenses",
    ),
    path(
        "monthly-payroll/",
        MonthlyPayrollAPIView.as_view(),
        name="monthly-payroll",
    ),
]