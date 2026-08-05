from django.urls import path

from .views import (
    DashboardKPIAPIView,
    MonthlyExpenseAPIView,
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
]